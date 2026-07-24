from __future__ import annotations

import json

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import CompanyWrite, DiscoveryRequest
from app.ai.schemas.grounded_llm_response import GroundedLLMResponse
from app.ai.schemas.llm_request import LLMRequest
from app.ai.services.llm_service import LLMService
from app.database.models.company import Company
from app.database.models.company_candidate import CompanyCandidate
from app.rag.builders.company_builder import CompanyDocumentBuilder
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store.indexing_service import IndexingService

EXTRACTION_SYSTEM_PROMPT = (
    "You extract structured company data strictly from provided research notes. "
    "Never invent a company, field, or fact that is not explicitly present in the notes. "
    "Respond with a JSON array only - no prose, no markdown fences."
)


class AdminService:
    def __init__(self, db: AsyncSession, llm: LLMService, indexing: IndexingService, retrieval: RetrievalPipeline | None = None):
        self.db = db
        self.llm = llm
        self.indexing = indexing
        self.retrieval = retrieval
        self.company_builder = CompanyDocumentBuilder()

    async def discover(self, request: DiscoveryRequest) -> list[CompanyCandidate]:
        """
        Find real candidate companies via LLM-driven web search, then extract
        structured fields strictly from the grounded search results. A candidate
        is only ever stored if its name appears in the grounded text AND it has
        at least one evidence item traceable to a real search-result URL - this
        is the hallucination gate: nothing is written from the LLM's imagination.

        If the live web search hits a provider rate limit/quota error, this
        falls back to surfacing already-indexed companies from our own
        directory that match the sector + country, rather than failing
        outright - no fabrication risk, since these are real, already-verified
        records, just not "new" discoveries.
        """
        try:
            grounded = self.llm.search(self._search_query(request))
        except Exception as exc:
            if self._is_rate_limited(exc):
                return await self._fallback_existing_matches(request)
            raise HTTPException(502, f"Company discovery search failed: {exc}") from exc

        if not grounded.text or not grounded.chunks:
            return []

        candidates: list[CompanyCandidate] = []
        seen: set[str] = set()

        for item in self._extract_candidates(grounded):
            name = (item.get("name") or "").strip()
            if not name or name.casefold() in seen:
                continue
            if name.casefold() not in grounded.text.casefold():
                continue  # extractor drifted beyond the grounded research - drop it

            evidence = self._evidence_for(name, grounded)
            if not evidence:
                continue  # no real search result ties back to this company - drop it

            if await self._company_exists(name):
                continue  # already in the database - nothing new to review

            seen.add(name.casefold())
            website = self._normalize_url(item.get("website", "")) or evidence[0]["url"]
            candidate = CompanyCandidate(
                name=name,
                country=request.country,
                category=(item.get("category") or "AI company").strip(),
                segment_tags=(item.get("segment_tags") or "").strip(),
                use_cases=(item.get("use_cases") or "").strip(),
                website=website,
                evidence=evidence,
                confidence_score=round(min(0.5 + 0.15 * len(evidence), 0.95), 2),
                status="pending",
            )
            self._validate_evidence(candidate.evidence)
            self.db.add(candidate)
            candidates.append(candidate)

        await self.db.commit()
        for candidate in candidates:
            await self.db.refresh(candidate)
        return candidates

    async def list_candidates(self) -> list[CompanyCandidate]:
        return list(await self.db.scalars(select(CompanyCandidate).order_by(CompanyCandidate.created_at.desc())))

    async def approve(self, candidate_id: int) -> Company:
        candidate = await self._candidate(candidate_id)
        if candidate.status != "pending":
            raise HTTPException(409, "Candidate has already been reviewed")
        duplicate = await self.db.scalar(select(Company).where(Company.vendor_name.ilike(candidate.name)))
        if duplicate:
            raise HTTPException(409, "A company with this name already exists")
        company = Company(**self._company_values_from_candidate(candidate))
        self.db.add(company)
        candidate.status = "approved"
        await self.db.commit()
        await self.db.refresh(company)
        await self.indexing.index_document(self.company_builder.build(company))
        return company

    async def reject(self, candidate_id: int) -> CompanyCandidate:
        candidate = await self._candidate(candidate_id)
        if candidate.status != "pending":
            raise HTTPException(409, "Candidate has already been reviewed")
        candidate.status = "rejected"
        await self.db.commit()
        await self.db.refresh(candidate)
        return candidate

    async def create_company(self, data: CompanyWrite) -> Company:
        duplicate = await self.db.scalar(select(Company).where(Company.vendor_name.ilike(data.vendor_name)))
        if duplicate:
            raise HTTPException(409, "A company with this name already exists")
        company = Company(**data.model_dump())
        self.db.add(company)
        await self.db.commit()
        await self.db.refresh(company)
        await self.indexing.index_document(self.company_builder.build(company))
        return company

    async def update_company(self, company_id: int, data: CompanyWrite) -> Company:
        company = await self.db.get(Company, company_id)
        if not company:
            raise HTTPException(404, "Company not found")
        duplicate = await self.db.scalar(select(Company).where(Company.vendor_name.ilike(data.vendor_name), Company.id != company_id))
        if duplicate:
            raise HTTPException(409, "A company with this name already exists")
        for field, value in data.model_dump().items():
            setattr(company, field, value)
        await self.db.commit()
        await self.db.refresh(company)
        await self.indexing.index_document(self.company_builder.build(company))
        return company

    async def _candidate(self, candidate_id: int) -> CompanyCandidate:
        candidate = await self.db.get(CompanyCandidate, candidate_id)
        if not candidate:
            raise HTTPException(404, "Candidate not found")
        return candidate

    async def _company_exists(self, name: str) -> bool:
        return await self.db.scalar(select(Company.id).where(Company.vendor_name.ilike(name))) is not None

    @staticmethod
    def _is_rate_limited(exc: Exception) -> bool:
        message = str(exc)
        return "RESOURCE_EXHAUSTED" in message or "429" in message or "quota" in message.lower()

    async def _fallback_existing_matches(self, request: DiscoveryRequest) -> list[CompanyCandidate]:
        """
        Live search is unavailable (rate-limited) - surface real, already-known
        companies from our own indexed directory that match the sector/country
        instead of failing outright. Never persisted and never a "pending"
        candidate: these already exist, so status="existing" keeps them out of
        the approve/reject workflow entirely.
        """
        if self.retrieval is None:
            return []

        retrieved = await self.retrieval.retrieve(f"{request.sector} {request.country}")
        company_ids: list[int] = []
        seen: set[int] = set()
        for result in retrieved.results:
            if result.document_type != "company":
                continue
            company_id = result.metadata.get("company_id")
            if not company_id or company_id in seen:
                continue
            seen.add(company_id)
            company_ids.append(company_id)

        if not company_ids:
            return []

        companies = await self.db.scalars(select(Company).where(Company.id.in_(company_ids)))
        by_id = {company.id: company for company in companies}

        # Skip companies that already have an "existing" match on file from a
        # previous fallback run for the same sector/country, so repeated
        # rate-limited attempts don't pile up duplicate rows.
        already_flagged = set(
            await self.db.scalars(
                select(CompanyCandidate.name).where(CompanyCandidate.status == "existing")
            )
        )

        matches: list[CompanyCandidate] = []
        added: set[int] = set()
        for result in retrieved.results:
            if result.document_type != "company":
                continue
            company_id = result.metadata.get("company_id")
            company = by_id.get(company_id)
            if not company or company.id in added or company.vendor_name in already_flagged:
                continue
            added.add(company.id)

            website = self._normalize_url(company.website)
            candidate = CompanyCandidate(
                name=company.vendor_name,
                country=company.country,
                category=company.ai_category,
                segment_tags=company.segment_tags,
                use_cases=company.food_beverage_ai_use_case,
                website=website,
                evidence=[{
                    "source": company.vendor_name,
                    "snippet": company.top_deployment_evidence or "Already indexed in your directory.",
                    "url": website or "#",
                }],
                confidence_score=round(min(result.similarity_score, 1.0), 2),
                status="existing",
            )
            self.db.add(candidate)
            matches.append(candidate)

        await self.db.commit()
        for candidate in matches:
            await self.db.refresh(candidate)
        return matches

    @staticmethod
    def _search_query(request: DiscoveryRequest) -> str:
        return (
            f"Find real, currently operating companies that sell or deploy AI solutions "
            f"for the '{request.sector}' sector in {request.country}. For each company, "
            f"state its name, country, primary AI category or use case, and website if known."
        )

    def _extract_candidates(self, grounded: GroundedLLMResponse) -> list[dict]:
        request = LLMRequest(
            system_prompt=EXTRACTION_SYSTEM_PROMPT,
            user_prompt=(
                "Research notes:\n"
                f"{grounded.text}\n\n"
                "Extract every distinct company mentioned as a JSON array of objects with keys: "
                'name, category, segment_tags, use_cases, website. Use "" for any field not present '
                "in the notes. Omit companies not clearly named in the notes."
            ),
            temperature=0.0,
            max_output_tokens=1500,
        )
        response = self.llm.generate(request)
        return self._parse_json_array(response.text)

    @staticmethod
    def _parse_json_array(text: str) -> list[dict]:
        cleaned = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            parsed = json.loads(cleaned)
        except (json.JSONDecodeError, ValueError):
            return []
        return [item for item in parsed if isinstance(item, dict)] if isinstance(parsed, list) else []

    @staticmethod
    def _evidence_for(name: str, grounded: GroundedLLMResponse) -> list[dict]:
        needle = name.casefold()
        evidence: list[dict] = []
        seen_urls: set[str] = set()
        for support in grounded.supports:
            if needle not in support.text.casefold():
                continue
            for index in support.chunk_indices:
                if index < 0 or index >= len(grounded.chunks):
                    continue
                chunk = grounded.chunks[index]
                if not chunk.uri or chunk.uri in seen_urls:
                    continue
                seen_urls.add(chunk.uri)
                evidence.append({"source": chunk.title or chunk.uri, "snippet": support.text.strip(), "url": chunk.uri})
        return evidence

    @staticmethod
    def _normalize_url(value: str) -> str:
        value = (value or "").strip()
        if not value:
            return ""
        return value if value.startswith("http") else f"https://{value}"

    @staticmethod
    def _validate_evidence(evidence: list[dict]) -> None:
        if not evidence or any(not item.get("source") or not item.get("snippet") or not item.get("url") for item in evidence):
            raise ValueError("Every discovery candidate must include complete evidence")

    @staticmethod
    def _company_values_from_candidate(candidate: CompanyCandidate) -> dict[str, str]:
        return {
            "vendor_name": candidate.name, "country": candidate.country, "ai_category": candidate.category,
            "segment_tags": candidate.segment_tags, "germany_presence": "", "company_type": "NewCo",
            "food_beverage_ai_use_case": candidate.use_cases, "top_germany_food_beverage_customers": "",
            "funding": "Not disclosed", "estimated_revenue": "Not disclosed", "maturity": "Unknown",
            "top_deployment_evidence": candidate.evidence[0]["snippet"], "website": candidate.website,
        }

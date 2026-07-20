from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.admin.schemas import CompanyWrite, DiscoveryRequest
from app.ai.services.llm_service import LLMService
from app.database.models.company import Company
from app.database.models.company_candidate import CompanyCandidate
from app.rag.builders.company_builder import CompanyDocumentBuilder
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline
from app.rag.vector_store.indexing_service import IndexingService


class AdminService:
    def __init__(self, db: AsyncSession, retrieval: RetrievalPipeline, llm: LLMService, indexing: IndexingService):
        self.db = db
        self.retrieval = retrieval
        self.llm = llm
        self.indexing = indexing
        self.company_builder = CompanyDocumentBuilder()

    async def discover(self, request: DiscoveryRequest) -> list[CompanyCandidate]:
        """Build reviewable candidates only from RAG-backed company records and evidence."""
        retrieved = await self.retrieval.retrieve(f"{request.sector} {request.country}")
        candidates: list[CompanyCandidate] = []
        seen: set[str] = set()

        for result in retrieved.results:
            metadata = result.metadata
            name = metadata.get("vendor_name")
            country = metadata.get("country")
            if result.document_type != "company" or not name or not country:
                continue
            if country.casefold() != request.country.casefold() or name.casefold() in seen:
                continue
            if request.sector.casefold() not in result.content.casefold():
                continue

            evidence_url = metadata.get("website")
            if not evidence_url:
                continue
            evidence_url = evidence_url if evidence_url.startswith("http") else f"https://{evidence_url}"
            seen.add(name.casefold())
            candidate = CompanyCandidate(
                name=name,
                country=country,
                category=metadata.get("ai_category", "AI company"),
                segment_tags=metadata.get("segment_tags", ""),
                use_cases=self._field(result.content, "Food & Beverage AI Use Cases"),
                website=evidence_url,
                evidence=[{"source": name, "snippet": self._field(result.content, "Deployment Evidence"), "url": evidence_url}],
                confidence_score=round(min(result.similarity_score, 1.0), 2),
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

    @staticmethod
    def _field(content: str, label: str) -> str:
        marker = f"{label}:\n"
        return content.split(marker, 1)[1].split("\n\n", 1)[0] if marker in content else ""

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

import json
from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.admin.schemas import DiscoveryRequest
from app.admin.service import AdminService
from app.ai.schemas.grounded_llm_response import GroundedLLMResponse, GroundingChunk, GroundingSupport
from app.ai.schemas.llm_response import LLMResponse


def test_evidence_validation_requires_source_snippet_and_url():
    with pytest.raises(ValueError):
        AdminService._validate_evidence([{"source": "Source", "snippet": "", "url": "https://example.com"}])


def test_candidate_maps_to_safe_company_defaults():
    candidate = SimpleNamespace(
        name="Example AI", country="Germany", category="Quality AI", segment_tags="1,2",
        use_cases="Inspection", website="https://example.com", evidence=[{"snippet": "Evidence"}],
    )
    values = AdminService._company_values_from_candidate(candidate)
    assert values["vendor_name"] == "Example AI"
    assert values["funding"] == "Not disclosed"
    assert values["top_deployment_evidence"] == "Evidence"


class DuplicateDatabase:
    async def get(self, model, candidate_id):
        return SimpleNamespace(id=candidate_id, name="Existing Co", status="pending")

    async def scalar(self, statement):
        return object()


@pytest.mark.asyncio
async def test_approval_rejects_duplicate_before_indexing():
    service = AdminService(DuplicateDatabase(), llm=None, indexing=None)
    with pytest.raises(HTTPException) as error:
        await service.approve(1)
    assert error.value.status_code == 409


class FakeDb:
    """Minimal AsyncSession stand-in: no existing companies, records what's added."""

    def __init__(self):
        self.added: list = []

    def add(self, obj):
        self.added.append(obj)

    async def commit(self):
        pass

    async def refresh(self, obj):
        pass

    async def scalar(self, statement):
        return None


class FakeDiscoveryLLM:
    """Stands in for LLMService: canned grounded search + canned extraction JSON."""

    def __init__(self, grounded: GroundedLLMResponse, extraction_text: str):
        self._grounded = grounded
        self._extraction_text = extraction_text

    def search(self, query: str) -> GroundedLLMResponse:
        return self._grounded

    def generate(self, request) -> LLMResponse:
        return LLMResponse(text=self._extraction_text, model="fake")


DISCOVERY_REQUEST = DiscoveryRequest(sector="Dairy Processing", country="Germany")


@pytest.mark.asyncio
async def test_discover_returns_empty_when_search_has_no_grounding():
    grounded = GroundedLLMResponse(text="", model="fake", chunks=[], supports=[])
    service = AdminService(FakeDb(), llm=FakeDiscoveryLLM(grounded, "[]"), indexing=None)

    result = await service.discover(DISCOVERY_REQUEST)

    assert result == []


@pytest.mark.asyncio
async def test_discover_drops_candidates_not_present_in_grounded_text():
    grounded = GroundedLLMResponse(
        text="Acme AI provides sorting robots for German dairies.",
        model="fake",
        chunks=[GroundingChunk(uri="https://acme.ai", title="Acme AI")],
        supports=[GroundingSupport(text="Acme AI provides sorting robots", start_index=0, end_index=32, chunk_indices=[0])],
    )
    extraction = json.dumps([{"name": "Ghost Corp", "category": "AI", "segment_tags": "", "use_cases": "", "website": ""}])
    service = AdminService(FakeDb(), llm=FakeDiscoveryLLM(grounded, extraction), indexing=None)

    result = await service.discover(DISCOVERY_REQUEST)

    assert result == []


@pytest.mark.asyncio
async def test_discover_drops_candidates_without_traceable_evidence():
    grounded = GroundedLLMResponse(
        text="Acme AI provides sorting robots for German dairies. Beta AI is also mentioned in passing.",
        model="fake",
        chunks=[GroundingChunk(uri="https://acme.ai", title="Acme AI")],
        supports=[GroundingSupport(text="Acme AI provides sorting robots", start_index=0, end_index=32, chunk_indices=[0])],
    )
    extraction = json.dumps([{"name": "Beta AI", "category": "AI", "segment_tags": "", "use_cases": "", "website": ""}])
    service = AdminService(FakeDb(), llm=FakeDiscoveryLLM(grounded, extraction), indexing=None)

    result = await service.discover(DISCOVERY_REQUEST)

    assert result == []


@pytest.mark.asyncio
async def test_discover_creates_candidate_with_grounded_evidence():
    grounded = GroundedLLMResponse(
        text="Acme AI provides sorting robots for German dairies.",
        model="fake",
        chunks=[GroundingChunk(uri="https://acme.ai", title="Acme AI")],
        supports=[GroundingSupport(
            text="Acme AI provides sorting robots for German dairies.", start_index=0, end_index=52, chunk_indices=[0],
        )],
    )
    extraction = json.dumps([{
        "name": "Acme AI", "category": "Sorting AI", "segment_tags": "2", "use_cases": "Sorting", "website": "acme.ai",
    }])
    service = AdminService(FakeDb(), llm=FakeDiscoveryLLM(grounded, extraction), indexing=None)

    result = await service.discover(DISCOVERY_REQUEST)

    assert len(result) == 1
    candidate = result[0]
    assert candidate.name == "Acme AI"
    assert candidate.website == "https://acme.ai"
    assert candidate.evidence == [{"source": "Acme AI", "snippet": "Acme AI provides sorting robots for German dairies.", "url": "https://acme.ai"}]
    # 1 distinct evidence source (0.15) + all fields present (0.15) + plausible
    # website (0.10) + independent corroboration that also matches the
    # extracted domain (0.40) = 0.80. Below the 0.90 auto-approve bar, so this
    # still lands in the human review queue.
    assert candidate.confidence_score == 0.80
    assert candidate.status == "pending"


class RateLimitedLLM:
    def search(self, query: str):
        raise Exception("429 RESOURCE_EXHAUSTED: quota exceeded for this project")


class BrokenLLM:
    def search(self, query: str):
        raise Exception("Something unrelated went wrong")


class FakeRetrievalPipeline:
    def __init__(self, results):
        self._results = results

    async def retrieve(self, query: str):
        return SimpleNamespace(results=self._results, context="")


class FakeRetrievalDb(FakeDb):
    """Answers the two scalars() calls _fallback_existing_matches makes, in order:
    first the matching Company rows, then any already-flagged candidate names."""

    def __init__(self, companies):
        super().__init__()
        self._scalars_queue = [companies, []]

    async def scalars(self, statement):
        return self._scalars_queue.pop(0)


@pytest.mark.asyncio
async def test_discover_falls_back_to_existing_matches_when_rate_limited():
    company = SimpleNamespace(
        id=42, vendor_name="Acme Dairy AI", country="Germany", ai_category="Dairy AI",
        segment_tags="1", food_beverage_ai_use_case="CIP monitoring",
        website="acme.example", top_deployment_evidence="Deployed at a major dairy plant.",
    )
    retrieval = FakeRetrievalPipeline([
        SimpleNamespace(document_type="company", metadata={"company_id": 42}, similarity_score=0.82),
    ])
    db = FakeRetrievalDb(companies=[company])
    service = AdminService(db, llm=RateLimitedLLM(), indexing=None, retrieval=retrieval)

    result = await service.discover(DISCOVERY_REQUEST)

    assert len(result) == 1
    assert result[0].name == "Acme Dairy AI"
    assert result[0].status == "existing"
    assert result[0].website == "https://acme.example"
    assert result[0].confidence_score == 0.82


@pytest.mark.asyncio
async def test_discover_fallback_returns_empty_without_retrieval_configured():
    service = AdminService(FakeDb(), llm=RateLimitedLLM(), indexing=None)

    result = await service.discover(DISCOVERY_REQUEST)

    assert result == []


@pytest.mark.asyncio
async def test_discover_raises_502_for_non_rate_limit_errors():
    service = AdminService(FakeDb(), llm=BrokenLLM(), indexing=None)

    with pytest.raises(HTTPException) as error:
        await service.discover(DISCOVERY_REQUEST)

    assert error.value.status_code == 502


class AutoApprovalDb(FakeDb):
    """
    Simulates just enough real-database behaviour for the auto-approve path:
    assigns a primary key and server-default timestamps on refresh(), the way
    a real commit would, so the auto-approved Company can be built into a
    KnowledgeDocument (which requires a non-null id and timestamps).
    """

    def __init__(self):
        super().__init__()
        self._next_id = 1

    async def refresh(self, obj):
        if getattr(obj, "id", None) is None:
            obj.id = self._next_id
            self._next_id += 1
        if getattr(obj, "created_at", None) is None:
            obj.created_at = datetime.now(UTC)
        if getattr(obj, "updated_at", None) is None:
            obj.updated_at = datetime.now(UTC)


class RecordingIndexingService:
    def __init__(self):
        self.indexed: list = []

    async def index_document(self, document):
        self.indexed.append(document)


class TwoStepLLM:
    """First search() call answers the primary discovery search; every call after answers corroboration."""

    def __init__(self, grounded, extraction_text, corroboration):
        self._grounded = grounded
        self._extraction_text = extraction_text
        self._corroboration = corroboration
        self.search_calls = 0

    def search(self, query: str):
        self.search_calls += 1
        return self._grounded if self.search_calls == 1 else self._corroboration

    def generate(self, request) -> LLMResponse:
        return LLMResponse(text=self._extraction_text, model="fake")


STRONG_GROUNDED = GroundedLLMResponse(
    text="Acme AI provides sorting robots for German dairies.",
    model="fake",
    chunks=[
        GroundingChunk(uri="https://acme.ai", title="Acme AI"),
        GroundingChunk(uri="https://foodtech-news.example/acme", title="Acme AI covered"),
        GroundingChunk(uri="https://industry-directory.example/acme", title="Acme AI listing"),
    ],
    supports=[
        GroundingSupport(
            text="Acme AI provides sorting robots for German dairies.",
            start_index=0, end_index=52, chunk_indices=[0, 1, 2],
        ),
    ],
)
STRONG_EXTRACTION = json.dumps([{
    "name": "Acme AI", "category": "Sorting AI", "segment_tags": "2",
    "use_cases": "Optical sorting for dairies", "website": "acme.ai",
}])


@pytest.mark.asyncio
async def test_discover_auto_approves_and_indexes_a_highly_corroborated_candidate():
    corroboration = GroundedLLMResponse(
        text="Acme AI is a real company providing optical sorting robots. Official site: acme.ai.",
        model="fake",
        chunks=[GroundingChunk(uri="https://acme.ai", title="Acme AI official site")],
    )
    indexing = RecordingIndexingService()
    llm = TwoStepLLM(STRONG_GROUNDED, STRONG_EXTRACTION, corroboration)
    service = AdminService(AutoApprovalDb(), llm=llm, indexing=indexing)

    result = await service.discover(DISCOVERY_REQUEST)

    assert len(result) == 1
    candidate = result[0]
    assert candidate.status == "auto_approved"
    assert candidate.confidence_score >= 0.90
    # The company was written straight to the directory and indexed for
    # search, with no human approval step involved.
    assert len(indexing.indexed) == 1
    assert indexing.indexed[0].metadata["vendor_name"] == "Acme AI"


@pytest.mark.asyncio
async def test_discover_keeps_candidate_pending_when_corroboration_search_is_rate_limited():
    class RateLimitedOnSecondCall(TwoStepLLM):
        def search(self, query: str):
            self.search_calls += 1
            if self.search_calls == 1:
                return self._grounded
            raise Exception("429 RESOURCE_EXHAUSTED: quota exceeded")

    indexing = RecordingIndexingService()
    llm = RateLimitedOnSecondCall(STRONG_GROUNDED, STRONG_EXTRACTION, corroboration=None)
    service = AdminService(AutoApprovalDb(), llm=llm, indexing=indexing)

    result = await service.discover(DISCOVERY_REQUEST)

    assert len(result) == 1
    candidate = result[0]
    # Strong evidence breadth/completeness/website alone cap at 0.60 - never
    # enough to auto-approve without the corroboration search succeeding.
    assert candidate.status == "pending"
    assert candidate.confidence_score <= 0.60
    assert indexing.indexed == []

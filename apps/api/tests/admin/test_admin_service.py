import json
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
    assert candidate.confidence_score == 0.65

from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.admin.service import AdminService


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
    service = AdminService(DuplicateDatabase(), retrieval=None, llm=None, indexing=None)
    with pytest.raises(HTTPException) as error:
        await service.approve(1)
    assert error.value.status_code == 409

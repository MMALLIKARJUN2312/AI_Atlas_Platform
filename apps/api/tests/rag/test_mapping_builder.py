from datetime import datetime, UTC

from app.models.problem_company_mapping import ProblemCompanyMapping
from app.rag.builders.mapping_builder import MappingDocumentBuilder
from app.rag.schemas.document_type import DocumentType


def test_mapping_document_builder():
    mapping = ProblemCompanyMapping(
        id=1,
        sequence_number=1,
        problem_statement="Seal integrity failure",
        segment_tags="Packaging",
        vc_stage="Production",
        ai_solution_1="Vision",
        ai_solution_2="ML",
        ai_solution_3="Automation",
        germany_vendors="Krones",
        roi_benchmark="20%",
        payback_months="12",
        regulatory_benefit="EU Compliance",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    document = MappingDocumentBuilder().build(mapping)

    assert document.document_type == DocumentType.MAPPING
    assert document.document_id == "mapping:1"
    assert "Krones" in document.content
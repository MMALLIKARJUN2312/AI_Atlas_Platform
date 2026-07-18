from datetime import datetime, UTC

from app.database.models.problem import Problem
from app.rag.builders.problem_builder import ProblemDocumentBuilder
from app.rag.schemas.document_type import DocumentType


def test_problem_document_builder():
    problem = Problem(
        id=1,
        problem_id="P-001",
        category="Packaging",
        problem_statement="Seal integrity failure",
        segment_tags="Packaging",
        vc_stage="Production",
        severity="5",
        ai_use_case_solution="Computer Vision",
        affected_germany_companies="Nestlé",
        financial_impact="€1M",
        regulatory_trigger="EU Food Safety",
        problem_type="Quality",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    document = ProblemDocumentBuilder().build(problem)

    assert document.document_type == DocumentType.PROBLEM
    assert document.document_id == "problem:1"
    assert "Seal integrity failure" in document.content
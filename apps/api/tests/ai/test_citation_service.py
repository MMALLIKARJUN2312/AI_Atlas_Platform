from app.ai.services.citation_service import CitationService
from app.rag.retrievers.retrieval_result import RetrievalResult


def test_citation_service_builds_company_source_from_retrieval_metadata():
    result = RetrievalResult(
        document_id="company:42",
        chunk_id="chunk-42",
        document_type="company",
        chunk_index=0,
        content="Vendor:\nKrones",
        metadata={"title": "Krones", "website": "krones.com"},
        similarity_score=0.95,
    )

    source = CitationService().build([result])[0]

    assert source.title == "Krones"
    assert source.source_type == "company"
    assert source.company_id == 42
    assert source.url == "https://krones.com"
    assert source.chunk_id == "chunk-42"


def test_citation_service_builds_problem_source_without_company_link():
    result = RetrievalResult(
        document_id="problem:9",
        chunk_id="chunk-9",
        document_type="problem",
        chunk_index=0,
        content="Problem Statement:\nCold chain temperature excursion",
        metadata={"title": "Cold chain temperature excursion"},
        similarity_score=0.95,
    )

    source = CitationService().build([result])[0]

    assert source.title == "Cold chain temperature excursion"
    assert source.company_id is None

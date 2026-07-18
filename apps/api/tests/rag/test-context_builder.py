from app.rag.retrievers.context_builder import ContextBuilder
from app.rag.retrievers.retrieval_result import RetrievalResult


def test_context_builder():

    builder = ContextBuilder()

    results = [
        RetrievalResult(
            document_id="1",
            chunk_id="c1",
            document_type="company",
            chunk_index=0,
            content="Google builds AI systems.",
            metadata={},
            similarity_score=0.9,
        )
    ]

    context = builder.build(results)

    assert "Google builds AI systems." in context
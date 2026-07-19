import pytest

from app.rag.retrievers.semantic_retriever import SemanticRetriever


class FakeEmbeddingService:

    def embed_query(self, query):
        return [0.1, 0.2]


class FakeRecord:

    document_id = "company:1"
    chunk_id = "chunk-1"
    document_type = "company"
    chunk_index = 0
    content = "Siemens is a global technology company."
    chunk_metadata = {"source": "companies.csv"}


class FakeVectorStore:

    async def similarity_search(self, embedding, top_k):
        return [
            (
                FakeRecord(),
                0.92,
            )
        ]


@pytest.mark.asyncio
async def test_semantic_retriever():

    retriever = SemanticRetriever(
        embedding_service=FakeEmbeddingService(),
        vector_store=FakeVectorStore(),
    )

    results = await retriever.retrieve(
        "What does Siemens do?"
    )

    assert len(results) == 1
    assert results[0].document_id == "company:1"
    assert results[0].similarity_score == 0.92
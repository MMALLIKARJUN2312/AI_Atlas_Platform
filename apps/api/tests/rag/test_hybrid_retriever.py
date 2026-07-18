from app.rag.retrievers.hybrid_retriever import HybridRetriever
from app.rag.retrievers.reciprocal_rank_fusion import ReciprocalRankFusion
from app.rag.retrievers.retrieval_result import RetrievalResult


class FakeSemanticRetriever:
    def retrieve(self, query, top_k):
        return [
            RetrievalResult(
                document_id="1",
                chunk_id="A",
                document_type="company",
                chunk_index=0,
                content="Semantic Result",
                metadata={},
                similarity_score=0.95,
            )
        ]


class FakeBM25Retriever:
    def retrieve(self, query, top_k):
        return [
            RetrievalResult(
                document_id="1",
                chunk_id="B",
                document_type="company",
                chunk_index=1,
                content="BM25 Result",
                metadata={},
                similarity_score=0.90,
            )
        ]


def test_hybrid_retriever():

    retriever = HybridRetriever(
        semantic_retriever=FakeSemanticRetriever(),
        bm25_retriever=FakeBM25Retriever(),
        fusion=ReciprocalRankFusion(),
    )

    results = retriever.retrieve("AI", top_k=10)

    assert len(results) == 2
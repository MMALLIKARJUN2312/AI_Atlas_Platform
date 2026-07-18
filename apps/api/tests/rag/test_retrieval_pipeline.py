from app.rag.retrievers.context_builder import ContextBuilder
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline
from app.rag.retrievers.retrieval_result import RetrievalResult


class FakeRetriever:

    def retrieve(self, query):

        return [
            RetrievalResult(
                document_id="1",
                chunk_id="c1",
                document_type="company",
                chunk_index=0,
                content="OpenAI develops GPT models.",
                metadata={},
                similarity_score=0.95,
            )
        ]


def test_retrieval_pipeline():

    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        context_builder=ContextBuilder(),
    )

    context = pipeline.retrieve_context("OpenAI")

    assert "OpenAI develops GPT models." in context
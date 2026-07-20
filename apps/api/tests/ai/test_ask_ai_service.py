import pytest

from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.schemas.ask_ai_response import AskAIResponse
from app.ai.schemas.llm_response import LLMResponse
from app.ai.services.llm_service import LLMService
from app.ai.services.ask_ai_service import AskAIService
from app.ai.services.citation_service import CitationService
from app.ai.services.response_validator import ResponseValidator
from app.rag.retrievers.context_builder import ContextBuilder
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline
from app.rag.retrievers.retrieval_result import RetrievalResult

class FakeRetriever:
    async def retrieve(self, query):
        return [
            RetrievalResult(
                document_id="company:1",
                chunk_id="chunk-1",
                document_type="company",
                chunk_index=0,
                content="Vendor:\nKrones\n\nGerman Customers:\nGerman beverage producers",
                metadata={"title": "Krones", "company_id": 1, "website": "krones.com"},
                similarity_score=0.99,
            )
        ]

class FakeLLM:
    def generate(self, request):
        return LLMResponse(text="Krones serves German beverage producers.", model="fake")

@pytest.mark.asyncio
async def test_ask_ai_service():

    pipeline = RetrievalPipeline(
        retriever=FakeRetriever(),
        context_builder=ContextBuilder(),
    )
    
    llm_service = LLMService(llm=FakeLLM(), validator=ResponseValidator())

    service = AskAIService(
        retrieval_pipeline=pipeline,
        prompt_builder=PromptBuilder(),
        llm_service=llm_service,
        citation_service=CitationService(),
    )

    response = await service.ask(
        "Who are Krones' German customers?"
    )

    assert isinstance(response, AskAIResponse)
    assert "Krones" in response.answer
    assert len(response.sources) == 1
    assert response.sources[0].title == "Krones"
    assert response.sources[0].company_id == 1
    assert response.sources[0].url == "https://krones.com"
    assert response.sources[0].chunk_id == "chunk-1"


class EmptyRetriever:
    async def retrieve(self, query):
        return []


@pytest.mark.asyncio
async def test_ask_ai_rejects_unknown_questions_without_calling_the_llm():
    service = AskAIService(
        retrieval_pipeline=RetrievalPipeline(retriever=EmptyRetriever(), context_builder=ContextBuilder()),
        prompt_builder=PromptBuilder(),
        llm_service=LLMService(llm=FakeLLM(), validator=ResponseValidator()),
        citation_service=CitationService(),
    )

    response = await service.ask("What is the weather in Berlin?")

    assert response.answer == "I don't have enough information to answer that question."
    assert response.sources == []

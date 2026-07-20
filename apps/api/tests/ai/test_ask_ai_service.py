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
                content="OpenAI develops GPT models.",
                metadata={},
                similarity_score=0.99,
            )
        ]

class FakeLLM:
    def generate(self, request):
        return LLMResponse(text="OpenAI develops GPT models.", model="fake")

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
        "What does OpenAI do?"
    )

    assert isinstance(response, AskAIResponse)
    assert "OpenAI" in response.answer
    assert len(response.citations) == 1
    assert response.citations[0].document_id == "company:1"
    assert response.citations[0].chunk_id == "chunk-1"

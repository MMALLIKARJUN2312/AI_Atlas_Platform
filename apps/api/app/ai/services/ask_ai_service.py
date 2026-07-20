from __future__ import annotations

from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.services.llm_service import LLMService
from app.ai.schemas.ask_ai_response import AskAIResponse
from app.ai.schemas.llm_request import LLMRequest
from app.ai.services.citation_service import CitationService
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline

class AskAIService:
    """
    End to end AI orchestration service
    """
    
    def __init__(self, retrieval_pipeline : RetrievalPipeline, prompt_builder : PromptBuilder, llm_service : LLMService, citation_service : CitationService):
        self.retrieval_pipeline = retrieval_pipeline
        self.prompt_builder = prompt_builder
        self.llm_service = llm_service
        self.citation_service = citation_service
        
    async def ask(self, question : str) -> AskAIResponse:
        retrieval = await self.retrieval_pipeline.retrieve(question)

        if not retrieval.results:
            return AskAIResponse(
                answer="I don't have enough information to answer that question.",
                sources=[],
            )

        prompt = self.prompt_builder.build(query=question, context=retrieval.context,)
        request = LLMRequest(system_prompt=prompt.system_prompt, user_prompt=prompt.user_prompt)
        llm_response = self.llm_service.generate(request)
        citations = self.citation_service.build(retrieval.results)

        return AskAIResponse(answer=llm_response.text, sources=citations)

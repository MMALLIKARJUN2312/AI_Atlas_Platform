from __future__ import annotations

from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.providers.base_llm import BaseLLM
from app.ai.schemas.ask_ai_response import AskAIResponse
from app.ai.services.citation_service import CitationService
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline

class AskAIService:
    """
    End to end AI orchestration service
    """
    
    def __init__(self, retrieval_pipeline : RetrievalPipeline, prompt_builder : PromptBuilder, llm : BaseLLM, citation_service : CitationService):
        self.retrieval_pipeline = retrieval_pipeline
        self.prompt_builder = prompt_builder
        self.llm = llm
        self.citation_service = citation_service
        
    def ask(self, question : str) -> AskAIResponse:
        retrieval = self.retrieval_pipeline.retrieve(question)
        prompt = self.prompt_builder.build(query=question, context=retrieval.context)
        answer = self.llm.generate(system_prompt=prompt.system_prompt, user_prompt=prompt.user_prompt)
        citations = self.citation_service.build(retrieval.results)
        
        return AskAIResponse(answer=answer, citations=citations)
    
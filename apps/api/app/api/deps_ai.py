from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_database
from app.ai.prompts.prompt_builder import PromptBuilder
from app.ai.providers.base_llm import BaseLLM
from app.ai.providers.llm_factory import LLMFactory
from app.ai.services.ask_ai_service import AskAIService
from app.ai.services.citation_service import CitationService
from app.ai.services.llm_service import LLMService
from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.embedders.embedder_factory import EmbedderFactory
from app.ai.services.response_validator import ResponseValidator
from app.core.config import settings
from app.ai.providers.llm_config import LLMConfig
from app.rag.retrievers.context_builder import ContextBuilder
from app.rag.retrievers.retrieval_pipeline import RetrievalPipeline
from app.rag.retrievers.semantic_retriever import SemanticRetriever
from app.rag.vector_store.pgvector_store import PGVectorStore


Database = Annotated[AsyncSession, Depends(get_database)]


def get_prompt_builder() -> PromptBuilder:
    return PromptBuilder()


def get_context_builder() -> ContextBuilder:
    return ContextBuilder()

def get_embedding_service() -> EmbeddingService:
    config = EmbeddingConfig(provider=settings.EMBEDDING_PROVIDER, model=settings.EMBEDDING_MODEL)

    embedder = EmbedderFactory.create(config)

    return EmbeddingService(embedder)

def get_vector_store(db: Database) -> PGVectorStore:
    return PGVectorStore(db)

def get_retriever(vector_store: PGVectorStore = Depends(get_vector_store), embedding_service: EmbeddingService = Depends(get_embedding_service)) -> SemanticRetriever:

    return SemanticRetriever(embedding_service=embedding_service, vector_store=vector_store)

def get_retrieval_pipeline(retriever: SemanticRetriever = Depends(get_retriever), context_builder: ContextBuilder = Depends(get_context_builder)) -> RetrievalPipeline:
    return RetrievalPipeline(retriever=retriever, context_builder=context_builder)

def get_llm() -> BaseLLM:
    config = LLMConfig(provider=settings.LLM_PROVIDER, model=settings.LLM_MODEL, api_key=settings.LLM_API_KEY)
    
    return LLMFactory.create(config)

def get_response_validator() -> ResponseValidator:
    return ResponseValidator()

def get_llm_service(llm: BaseLLM = Depends(get_llm), validator: ResponseValidator = Depends(get_response_validator)) -> LLMService:
    return LLMService(llm=llm, validator=validator)

def get_citation_service() -> CitationService:
    return CitationService()

def get_ask_ai_service(
    retrieval_pipeline: RetrievalPipeline = Depends(get_retrieval_pipeline),
    prompt_builder: PromptBuilder = Depends(get_prompt_builder),
    llm_service: LLMService = Depends(get_llm_service),
    citation_service: CitationService = Depends(get_citation_service),
) -> AskAIService:
    return AskAIService(
        retrieval_pipeline=retrieval_pipeline,
        prompt_builder=prompt_builder,
        llm_service=llm_service,
        citation_service=citation_service,
    )
    


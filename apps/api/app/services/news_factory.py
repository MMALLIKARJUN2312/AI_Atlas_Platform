from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps_ai import get_embedding_service
from app.rag.chunkers.recursive_chunker import RecursiveChunker
from app.rag.vector_store.indexing_service import IndexingService
from app.rag.vector_store.pgvector_store import PGVectorStore
from app.repositories.company_repository import CompanyRepository
from app.repositories.news_repository import NewsRepository
from app.services.news_service import NewsService


def build_news_service(db: AsyncSession) -> NewsService:
    indexing_service = IndexingService(
        chunker=RecursiveChunker(),
        embedding_service=get_embedding_service(),
        vector_store=PGVectorStore(db),
    )
    return NewsService(NewsRepository(db), CompanyRepository(db), indexing_service)

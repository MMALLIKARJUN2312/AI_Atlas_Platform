from app.core.event_loop import configure_event_loop

configure_event_loop()

import asyncio

from time import perf_counter

from app.database.session import AsyncSessionLocal
from app.services.dataset_import_service import DatasetImportService
from app.services.dataset_indexing_service import DatasetIndexingService
from app.rag.chunkers.recursive_chunker import RecursiveChunker
from app.rag.embedders.gemini_embedder import GeminiEmbedder
from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.embedders.embedder_factory import EmbedderFactory
from app.rag.vector_store.pgvector_store import PGVectorStore
from app.rag.vector_store.indexing_service import IndexingService
from app.rag.vector_store.vector_config import VectorConfig

async def main() -> None:
    start = perf_counter()

    async with AsyncSessionLocal() as session:

        #Import CSVs
        importer = DatasetImportService(session)
        import_summary = await importer.import_all()

        #Build Indexing Pipeline
        chunker = RecursiveChunker()

        embedding_config = EmbeddingConfig(
            provider="gemini",
            model=VectorConfig.EMBEDDING_MODEL,
            dimensions=VectorConfig.EMBEDDING_DIMENSIONS,
        )

        embedder = EmbedderFactory.create(embedding_config)

        embedding_service = EmbeddingService(embedder)
        vector_store = PGVectorStore(session)

        indexing_service = IndexingService(chunker=chunker, embedding_service=embedding_service, vector_store=vector_store)

        dataset_indexer = DatasetIndexingService(db=session, indexing_service=indexing_service,)

        indexing_summary = await dataset_indexer.index_all()

    elapsed = perf_counter() - start

    print(import_summary)
    print(indexing_summary)
    print(f"Completed in {elapsed:.2f} seconds")
    
if __name__ == "__main__":
    asyncio.run(main())
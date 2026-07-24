import pytest
from datetime import datetime, UTC

from app.rag.vector_store.indexing_service import IndexingService
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.schemas.embedded_chunk import EmbeddedChunk


from app.rag.schemas.knowledge_chunk import KnowledgeChunk


class FakeChunker:

    def chunk(self, document):

        return [
            KnowledgeChunk(
                chunk_id="chunk-1",
                document_id=document.document_id,
                document_type=document.document_type,
                chunk_index=0,
                text=document.content,
                metadata=document.metadata,
            )
        ]
class FakeEmbeddingService:

    def __init__(self):
        self.generate_calls = 0

    def generate(self, chunks):
        self.generate_calls += 1
        return [
            EmbeddedChunk(
                chunk=chunks[0],
                embedding=[0.1, 0.2],
                model="fake-model",
                dimensions=2,
            )
        ]


class FakeVectorStore:

    def __init__(self, existing_chunks=None):
        self.called = False
        self._existing_chunks = existing_chunks or []

    async def get_document_chunks(self, document_id):
        return self._existing_chunks

    async def reindex_document(self, chunks):
        self.called = True


@pytest.mark.asyncio
async def test_indexing_service():

    document = KnowledgeDocument(
        document_id="company:1",
        document_type=DocumentType.COMPANY,
        source_id=1,
        title="Company",
        content="Some content",
        metadata={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    vector_store = FakeVectorStore()

    service = IndexingService(
        chunker=FakeChunker(),
        embedding_service=FakeEmbeddingService(),
        vector_store=vector_store,
    )

    await service.index_document(document)

    assert vector_store.called is True


@pytest.mark.asyncio
async def test_indexing_service_skips_reembedding_when_content_unchanged():
    from types import SimpleNamespace

    document = KnowledgeDocument(
        document_id="company:1",
        document_type=DocumentType.COMPANY,
        source_id=1,
        title="Company",
        content="Some content",
        metadata={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # Same content already stored under this document_id, at chunk_index 0.
    existing = [SimpleNamespace(chunk_index=0, content="Some content")]
    vector_store = FakeVectorStore(existing_chunks=existing)
    embedding_service = FakeEmbeddingService()

    service = IndexingService(
        chunker=FakeChunker(),
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    await service.index_document(document)

    assert embedding_service.generate_calls == 0
    assert vector_store.called is False


@pytest.mark.asyncio
async def test_indexing_service_reembeds_when_content_changed():
    from types import SimpleNamespace

    document = KnowledgeDocument(
        document_id="company:1",
        document_type=DocumentType.COMPANY,
        source_id=1,
        title="Company",
        content="New content",
        metadata={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    # Stored content differs from the freshly-built document's content.
    existing = [SimpleNamespace(chunk_index=0, content="Old content")]
    vector_store = FakeVectorStore(existing_chunks=existing)
    embedding_service = FakeEmbeddingService()

    service = IndexingService(
        chunker=FakeChunker(),
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    await service.index_document(document)

    assert embedding_service.generate_calls == 1
    assert vector_store.called is True
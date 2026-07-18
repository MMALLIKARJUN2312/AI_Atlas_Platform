from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.embedded_chunk import EmbeddedChunk
from app.rag.schemas.document_type import DocumentType
from app.rag.vector_store.indexing_service import IndexingService

from datetime import datetime, UTC


class FakeChunker:

    def chunk(self, document):
        return [
            KnowledgeChunk(
                chunk_id="chunk-1",
                document_id=document.document_id,
                chunk_index=0,
                text=document.content,
                metadata=document.metadata,
            )
        ]


class FakeEmbedder:

    def embed(self, chunks):
        return [
            EmbeddedChunk(
                chunk=chunks[0],
                embedding=[0.1, 0.2],
                model="fake",
                dimensions=2,
            )
        ]


class FakeVectorStore:

    def __init__(self):
        self.called = False

    def reindex_document(self, embedded_chunks):
        self.called = True


def test_indexing_service():

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
        embedder=FakeEmbedder(),
        vector_store=vector_store,
    )

    service.index_document(document)

    assert vector_store.called
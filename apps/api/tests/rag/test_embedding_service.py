from datetime import datetime, UTC

from app.rag.embedders.embedding_config import EmbeddingConfig
from app.rag.embedders.embedding_service import EmbeddingService
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.embedded_chunk import EmbeddedChunk
from app.rag.schemas.knowledge_chunk import KnowledgeChunk
from app.rag.schemas.knowledge_document import KnowledgeDocument

class FakeEmbedder:

    def embed(self, chunks):
        return [
            EmbeddedChunk(
                chunk=chunks[0],
                embedding=[0.1, 0.2],
                model="fake-model",
                dimensions=2,
            )
        ]

    def embed_query(self, query: str):
        return [0.1, 0.2]

def test_embedding_service_generate():
    document = KnowledgeDocument(
        document_id="company:1",
        document_type=DocumentType.COMPANY,
        source_id=1,
        title="Sample Company",
        content="Sample content",
        metadata={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    chunk = KnowledgeChunk(
        chunk_id="chunk-1",
        document_id=document.document_id,
        chunk_index=0,
        text=document.content,
        metadata=document.metadata,
    )

    service = EmbeddingService(config=EmbeddingConfig())

    # Replace the real provider with a fake one.
    service.embedder = FakeEmbedder()

    embedded_chunks = service.generate([chunk])

    assert len(embedded_chunks) == 1
    assert embedded_chunks[0].chunk.chunk_id == "chunk-1"
    assert embedded_chunks[0].model == "fake-model"
    assert embedded_chunks[0].dimensions == 2
    assert embedded_chunks[0].embedding == [0.1, 0.2]
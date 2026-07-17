from datetime import datetime, UTC

from app.rag.chunkers.recursive_chunker import RecursiveChunker
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument


def test_recursive_chunker():

    document = KnowledgeDocument(
        document_id="company:1",
        document_type=DocumentType.COMPANY,
        source_id=1,
        title="Sample Company",
        content="Lorem ipsum " * 300,
        metadata={},
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    chunker = RecursiveChunker()

    chunks = chunker.chunk(document)

    assert len(chunks) > 1
    assert chunks[0].document_id == "company:1"
    assert chunks[0].chunk_index == 0
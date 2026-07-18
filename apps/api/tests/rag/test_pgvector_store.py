from unittest.mock import MagicMock

from app.rag.vector_store.pgvector_store import PGVectorStore


def test_delete_document():
    session = MagicMock()
    store = PGVectorStore(session)
    store.delete_document("company-1")
    session.execute.assert_called_once()
    session.commit.assert_called_once()
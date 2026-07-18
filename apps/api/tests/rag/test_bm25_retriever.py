from app.rag.retrievers.bm25_retriever import BM25Retriever
from unittest.mock import MagicMock


def test_bm25_retriever_creation():

    session = MagicMock()
    retriever = BM25Retriever(session)

    assert retriever.db == session
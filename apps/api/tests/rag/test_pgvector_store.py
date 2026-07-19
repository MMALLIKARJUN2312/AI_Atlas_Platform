import pytest
from unittest.mock import AsyncMock

from app.rag.vector_store.pgvector_store import PGVectorStore


@pytest.mark.asyncio
async def test_delete_document():

    session = AsyncMock()
    store = PGVectorStore(session)

    await store.delete_document("company-1")

    session.execute.assert_called_once()
    session.commit.assert_called_once()
from fastapi.testclient import TestClient

from app.main import app
from app.api.deps_ai import get_ask_ai_service

from app.ai.schemas.ask_ai_response import AskAIResponse
from app.ai.schemas.citation import Source


class FakeAskAIService:

    async def ask(
        self,
        question: str,
    ) -> AskAIResponse:

        return AskAIResponse(
            answer="OpenAI develops GPT models.",
            sources=[
                Source(
                    title="Krones",
                    source_type="company",
                    company_id=1,
                    url="https://krones.com",
                    chunk_id="chunk-1",
                )
            ],
        )

app.dependency_overrides[get_ask_ai_service] = (
    lambda: FakeAskAIService()
)

client = TestClient(app)


def test_ask_ai_success():

    response = client.post(
        "/api/v1/ai/ask",
        json={
            "question": "What is OpenAI?"
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["answer"] == "OpenAI develops GPT models."

    assert body["sources"] == [
        {
            "title": "Krones",
            "source_type": "company",
            "company_id": 1,
            "url": "https://krones.com",
            "chunk_id": "chunk-1",
        }
    ]

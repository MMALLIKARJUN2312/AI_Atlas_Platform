from app.ai.providers.gemini_llm import GeminiLLM
from app.ai.providers.llm_factory import LLMFactory


def test_llm_factory():

    llm = LLMFactory.create(
        provider="gemini",
        model="gemini-2.5-flash",
    )

    assert isinstance(llm, GeminiLLM)
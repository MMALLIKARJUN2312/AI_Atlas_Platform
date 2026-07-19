from app.ai.providers.llm_config import LLMConfig
from app.ai.providers.gemini_llm import GeminiLLM
from app.ai.providers.llm_factory import LLMFactory


def test_llm_factory():

    config = LLMConfig(
        provider="gemini",
        model="gemini-2.5-flash",
    )

    llm = LLMFactory.create(config)

    assert isinstance(llm, GeminiLLM)
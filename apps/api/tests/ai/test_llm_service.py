from app.ai.schemas.llm_request import LLMRequest
from app.ai.schemas.llm_response import LLMResponse
from app.ai.services.llm_service import LLMService
from app.ai.services.response_validator import ResponseValidator


class FakeLLM:

    def generate(
        self,
        *,
        system_prompt,
        user_prompt,
    ):

        return LLMResponse(
            text="Hello World",
            model="fake",
        )


def test_llm_service():

    service = LLMService(
        llm=FakeLLM(),
        validator=ResponseValidator(),
    )

    request = LLMRequest(
        system_prompt="system",
        user_prompt="user",
    )
    
    response = service.generate(request)

    assert response.text == "Hello World"
    assert response.model == "fake"
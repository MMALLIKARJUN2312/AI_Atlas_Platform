from app.ai.schemas.llm_response import LLMResponse

class ResponseValidator:
    """
    Validates LLM responses before returning them
    """

    def validate(self, response : LLMResponse) -> LLMResponse:
        response.text = response.text.strip()

        if not response.text:
            raise ValueError("LLM returned an empty response")

        return response

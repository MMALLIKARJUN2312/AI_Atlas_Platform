from pydantic import BaseModel, Field


class LLMRequest(BaseModel):
    """
    Normalized request sent to an LLM provider.
    """

    system_prompt: str
    user_prompt: str
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_output_tokens: int = Field(default=1024, gt=0)
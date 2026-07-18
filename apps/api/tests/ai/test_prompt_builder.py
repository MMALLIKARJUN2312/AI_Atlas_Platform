from app.ai.prompts.prompt_builder import PromptBuilder


def test_prompt_builder():

    builder = PromptBuilder()

    prompt = builder.build(
        query="What does OpenAI do?",
        context="OpenAI develops GPT models.",
    )

    assert "OpenAI develops GPT models." in prompt.user_prompt
    assert "What does OpenAI do?" in prompt.user_prompt
    assert len(prompt.system_prompt) > 100
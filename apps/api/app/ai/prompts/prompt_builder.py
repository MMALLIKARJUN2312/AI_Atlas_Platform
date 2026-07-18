from __future__ import annotations

from app.ai.prompts.prompt_template import PromptTemplate
from app.ai.prompts.system_prompt import SYSTEM_PROMPT

class PromptBuilder:
    """
    Builds prompts for the LLM
    """
    
    def build(self, *, query : str, context : str) -> PromptTemplate:
        user_prompt = f"""
Context : 
{context}

---------------------------

Question :
{query}

Answer using ONLY the provided context
""".strip()

        return PromptTemplate(system_prompt=SYSTEM_PROMPT, user_prompt=user_prompt)
from __future__ import annotations

from app.ai.prompts.prompt_template import PromptTemplate
from app.ai.prompts.system_prompt import SYSTEM_PROMPT


class PromptBuilder:
    """
    Builds prompts for grounded QA.
    """

    def build(
        self,
        *,
        query: str,
        context: str,
    ) -> PromptTemplate:

        user_prompt = f"""
You are answering questions using ONLY the provided knowledge base.

================ KNOWLEDGE BASE ================

{context}

================================================

Question:
{query}

Instructions:

- Answer ONLY using the knowledge base.
- Never use outside knowledge.
- If the answer is not present, explicitly say you don't have enough information.
- Never invent companies, products or facts.
- Prefer concise but complete answers.
- When multiple companies satisfy the query, summarize them clearly.
"""

        return PromptTemplate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt.strip(),
        )
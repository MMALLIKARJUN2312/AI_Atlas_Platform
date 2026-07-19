from __future__ import annotations

from collections import defaultdict

from app.rag.retrievers.retrieval_result import RetrievalResult


class ContextBuilder:
    """
    Builds structured context for the LLM.
    Groups retrieved documents by document type.
    """

    def build(self, results: list[RetrievalResult]) -> str:

        if not results:
            return "No relevant context found."

        grouped: dict[str, list[RetrievalResult]] = defaultdict(list)

        for result in results:
            grouped[result.document_type].append(result)

        sections: list[str] = []

        order = ["sector", "problem", "mapping", "company", "news",]

        for document_type in order:

            documents = grouped.get(document_type)

            if not documents:
                continue

            sections.append(f"========== {document_type.upper()} ==========")

            for document in documents:

                sections.append(document.content.strip())

                sections.append("")

        remaining = set(grouped.keys()) - set(order)

        for document_type in sorted(remaining):

            sections.append(f"========== {document_type.upper()} ==========")

            for document in grouped[document_type]:

                sections.append(document.content.strip())

                sections.append("")

        return "\n".join(sections).strip()
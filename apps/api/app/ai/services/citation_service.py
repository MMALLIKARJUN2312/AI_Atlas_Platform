from __future__ import annotations

from app.ai.schemas.citation import Source
from app.rag.retrievers.retrieval_result import RetrievalResult

class CitationService:
    """
    Builds user-facing source references from retrieved chunks.
    """
    
    def build(self, results: list[RetrievalResult]) -> list[Source]:
        sources = []
        
        seen : set[tuple[str, str]] = set()
        
        for result in results:
            key = (result.document_id, result.chunk_id)
            
            if key in seen:
                continue
            
            seen.add(key)
            
            metadata = result.metadata
            source_type = result.document_type
            company_id = metadata.get("company_id")

            if source_type == "company":
                company_id = self._document_source_id(result.document_id)

            sources.append(
                Source(
                    title=str(metadata.get("title") or self._title_from_content(result)),
                    source_type=source_type,
                    company_id=company_id,
                    url=self._normalise_url(metadata.get("source_url") or metadata.get("website")),
                    chunk_id=result.chunk_id,
                )
            )

        return sources

    @staticmethod
    def _document_source_id(document_id: str) -> int | None:
        try:
            return int(document_id.rsplit(":", 1)[1])
        except (IndexError, ValueError):
            return None

    @staticmethod
    def _title_from_content(result: RetrievalResult) -> str:
        for line in result.content.splitlines():
            if ":" in line:
                _, value = line.split(":", 1)
                if value.strip():
                    return value.strip()
        return result.document_id

    @staticmethod
    def _normalise_url(url: object) -> str | None:
        if not isinstance(url, str) or not url.strip():
            return None
        url = url.strip()
        return url if url.startswith(("http://", "https://")) else f"https://{url}"

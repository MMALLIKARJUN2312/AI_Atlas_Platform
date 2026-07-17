from __future__ import annotations

from collections.abc import Iterable

class DocumentComposer:
    """
    Builds consistently formatted text documents for the RAG pipeline.
    
    Each section is rendered as :
    Section Title : Value
    """
    
    @staticmethod
    def compose(sections : Iterable[tuple[str, object | None]]) -> str:
        blocks : list[str] = []
        
        for title, value in sections:
            if value is None:
                continue
            
            text = str(value).strip()
            
            if not text:
                continue
            
            blocks.append(f"{title}:\n{text}")
            
        return "\n\n".join(blocks)
    
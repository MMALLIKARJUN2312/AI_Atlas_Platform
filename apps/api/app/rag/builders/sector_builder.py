from __future__ import annotations

from app.database.models.sector import Sector
from app.rag.builders.base_builder import BaseDocumentBuilder
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.utils import DocumentComposer

class SectorDocumentBuilder(BaseDocumentBuilder[Sector]):
    
    def build(self, sector : Sector) -> KnowledgeDocument:
        content = DocumentComposer.compose(
            [
                ("Segment Number", sector.segment_number),
                ("Segment Name", sector.segment_name),
                ("Definition", sector.definition),
                ("Key German Companies", sector.key_germany_companies),
                ("AI Adoption", sector.ai_adoption),
                ("Market Size", sector.de_market_size),
                ("Regulatory Complexity", sector.regulatory_complexity),
                ("Platform Priority", sector.platform_priority),
                ("Primary AI Entry Point", sector.primary_ai_entry_point)        
            ]
        )

        metadata = {
            "segment_name" : sector.segment_name,
            "segment_number" : sector.segment_number,
            "ai_adoption" : sector.ai_adoption
        }
        
        return KnowledgeDocument(
            document_id=f"sector:{sector.id}",
            document_type=DocumentType.SECTOR,
            source_id=sector.id,
            title=sector.segment_name,
            content=content,
            metadata=metadata,
            created_at=sector.created_at,
            updated_at=sector.updated_at
        )
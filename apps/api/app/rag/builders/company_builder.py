from __future__ import annotations

from app.database.models.company import Company
from app.rag.builders.base_builder import BaseDocumentBuilder
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.utils.document_composer import DocumentComposer

class CompanyDocumentBuilder(BaseDocumentBuilder[Company]):
    
    def build(self, company : Company) -> KnowledgeDocument:
        content = DocumentComposer.compose(
            [
                ("Vendor", company.vendor_name),
                ("Country", company.country),
                ("AI Category", company.ai_category),
                ("Segments", company.segment_tags),
                ("Germany Presence", company.germany_presence),
                ("Company Type", company.company_type),
                ("Food & Beverage AI Use Cases", company.food_beverage_ai_use_case),
                ("German Customers", company.top_germany_food_beverage_customers),
                ("Funding", company.funding),
                ("Estimated Revenue", company.estimated_revenue),
                ("Maturity", company.maturity),
                ("Deployment Evidence", company.top_deployment_evidence),
                ("Website", company.website)        
            ]
        )

        metadata = {
            "vendor_name" : company.vendor_name,
            "country" : company.country,
            "company_type" : company.company_type,
            "segment_tags" : company.segment_tags,
            "website" : company.website
        }
        
        return KnowledgeDocument(
            document_id=f"company:{company.id}",
            document_type=DocumentType.COMPANY,
            source_id=company.id,
            title=company.vendor_name,
            content=content,
            metadata=metadata,
            created_at=company.created_at,
            updated_at=company.updated_at
        )
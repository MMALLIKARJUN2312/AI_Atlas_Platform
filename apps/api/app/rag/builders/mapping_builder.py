from __future__ import annotations

from app.database.models.problem_company_mapping import ProblemCompanyMapping
from app.rag.builders.base_builder import BaseDocumentBuilder
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.utils import DocumentComposer

class MappingDocumentBuilder(BaseDocumentBuilder[ProblemCompanyMapping]):
    
    def build(self, mapping: ProblemCompanyMapping) -> KnowledgeDocument:
        content = DocumentComposer.compose(
            [
                ("Problem Statement", mapping.problem_statement),
                ("Segment Tags", mapping.segment_tags),
                ("Value Chain Stage", mapping.vc_stage),
                ("AI Solution 1", mapping.ai_solution_1),
                ("AI Solution 2", mapping.ai_solution_2),
                ("AI Solution 3", mapping.ai_solution_3),
                ("German Vendors", mapping.germany_vendors),
                ("ROI Benchmark", mapping.roi_benchmark),
                ("Payback Months", mapping.payback_months),
                ("Regulatory Benefit", mapping.regulatory_benefit)                        
            ]
        )

        metadata = {
            "segment_tags" : mapping.segment_tags,
            "vc_stage" : mapping.vc_stage,
            "payback_months" : mapping.payback_months
        }
        
        return KnowledgeDocument(
            document_id=f"mapping:{mapping.id}",
            document_type=DocumentType.MAPPING,
            source_id=mapping.id,
            title=mapping.problem_statement,
            content=content,
            metadata=metadata,
            created_at=mapping.created_at,
            updated_at=mapping.updated_at
        )
from __future__ import annotations

from app.database.models.problem import Problem
from app.rag.builders.base_builder import BaseDocumentBuilder
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.utils import DocumentComposer

class ProblemDocumentBuilder(BaseDocumentBuilder[Problem]):
    
    def build(self, problem : Problem) -> KnowledgeDocument:
        content = DocumentComposer.compose(
            [
                ("Problem ID", problem.problem_id),
                ("Category", problem.category),
                ("Problem Statement", problem.problem_statement),
                ("Segment Tags", problem.segment_tags),
                ("Value Chain Stage", problem.vc_stage),
                ("Severity", problem.severity),
                ("AI Solution", problem.ai_use_case_solution),
                ("Affected German Companies", problem.affected_germany_companies),
                ("Financial Impact", problem.financial_impact),
                ("Regulatory Trigger", problem.regulatory_trigger),
                ("Problem Type", problem.problem_type)        
            ]
        )

        metadata = {
            "title": problem.problem_statement,
            "problem_id" : problem.problem_id,
            "category" : problem.category,
            "severity" : problem.severity,
            "segment_tags" : problem.segment_tags,
            "problem_type" : problem.problem_type
        }
        
        return KnowledgeDocument(
            document_id=f"problem:{problem.id}",
            document_type=DocumentType.PROBLEM,
            source_id=problem.id,
            title=problem.problem_statement,
            content=content,
            metadata=metadata,
            created_at=problem.created_at,
            updated_at=problem.updated_at
        )

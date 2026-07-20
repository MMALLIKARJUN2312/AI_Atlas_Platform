from app.database.models.news import News
from app.rag.builders.base_builder import BaseDocumentBuilder
from app.rag.schemas.document_type import DocumentType
from app.rag.schemas.knowledge_document import KnowledgeDocument
from app.rag.utils.document_composer import DocumentComposer


class NewsDocumentBuilder(BaseDocumentBuilder[News]):
    def build(self, news: News) -> KnowledgeDocument:
        content = DocumentComposer.compose(
            [
                ("Headline", news.title),
                ("Summary", news.summary),
                ("Source", news.source_name),
                ("Published", news.published_at.isoformat()),
                ("URL", news.source_url),
            ]
        )
        return KnowledgeDocument(
            document_id=f"news:{news.id}",
            document_type=DocumentType.NEWS,
            source_id=news.id,
            title=news.title,
            content=content,
            metadata={
                "type": "news",
                "company_id": news.company_id,
                "source_url": news.source_url,
                "published_at": news.published_at.isoformat(),
            },
            created_at=news.created_at,
            updated_at=news.updated_at,
        )

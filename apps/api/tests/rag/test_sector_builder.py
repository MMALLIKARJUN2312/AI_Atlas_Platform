from datetime import datetime, UTC

from app.models.sector import Sector
from app.rag.builders.sector_builder import SectorDocumentBuilder
from app.rag.schemas.document_type import DocumentType


def test_sector_document_builder():
    sector = Sector(
        id=1,
        segment_number=1,
        segment_name="Packaging",
        definition="Packaging Industry",
        key_germany_companies="Krones",
        ai_adoption="High",
        de_market_size="€50B",
        regulatory_complexity="High",
        platform_priority="High",
        primary_ai_entry_point="Inspection",
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC),
    )

    document = SectorDocumentBuilder().build(sector)

    assert document.document_type == DocumentType.SECTOR
    assert document.document_id == "sector:1"
    assert document.title == "Packaging"
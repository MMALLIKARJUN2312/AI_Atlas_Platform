from sqlalchemy import JSON, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.database.models.mixins import TimestampMixin


class CompanyCandidate(TimestampMixin, Base):
    __tablename__ = "company_candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    country: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(Text)
    segment_tags: Mapped[str] = mapped_column(Text)
    use_cases: Mapped[str] = mapped_column(Text)
    website: Mapped[str] = mapped_column(String(255))
    evidence: Mapped[list[dict]] = mapped_column(JSON)
    confidence_score: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="pending", index=True)

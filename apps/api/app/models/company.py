from sqlalchemy import Integer, String, Float, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 
from app.models.mixins import TimestampMixin

class Company(TimestampMixin, Base):
    __tablename__ = "companies"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    country : Mapped[str] = mapped_column(String(100))
    website : Mapped[str] = mapped_column(String(500))
    company_type : Mapped[str] = mapped_column(String(100))
    ai_category : Mapped[str] = mapped_column(String(255))
    segment_tags : Mapped[str] = mapped_column(Text)
    germany_presence : Mapped[str] = mapped_column(String(255))
    use_cases : Mapped[str] = mapped_column(Text)
    customers : Mapped[str] = mapped_column(Text)
    funding : Mapped[str] = mapped_column(String(255))
    estimated_revenue : Mapped[str] = mapped_column(String(255))
    maturity : Mapped[int] = mapped_column(Integer)
    deployment_evidence : Mapped[int] = mapped_column(Text)
    confidence_score : Mapped[float] = mapped_column(Float, default=1.0)
    approved : Mapped[bool] = mapped_column(default=True)
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base 
from app.database.models.mixins import TimestampMixin

class Company(TimestampMixin, Base):
    __tablename__ = "companies"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    vendor_name : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    country : Mapped[str] = mapped_column(String(100))
    ai_category : Mapped[str] = mapped_column(Text)
    segment_tags : Mapped[str] = mapped_column(Text)
    germany_presence : Mapped[str] = mapped_column(Text)
    company_type : Mapped[str] = mapped_column(String(100))
    food_beverage_ai_use_case : Mapped[str] = mapped_column(Text)
    top_germany_food_beverage_customers : Mapped[str] = mapped_column(Text)
    funding : Mapped[str] = mapped_column(String(255))
    estimated_revenue : Mapped[str] = mapped_column(String(255))
    maturity : Mapped[str] = mapped_column(String(100))
    top_deployment_evidence : Mapped[str] = mapped_column(Text)
    website : Mapped[str] = mapped_column(String(255))    
    news: Mapped[list["News"]] = relationship(back_populates="company", cascade="all, delete-orphan")

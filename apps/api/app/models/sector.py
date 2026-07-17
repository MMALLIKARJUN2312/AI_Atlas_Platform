from sqlalchemy import String, Text 
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 
from app.models.mixins import TimestampMixin

class Sector(TimestampMixin, Base):
    __tablename__ = "sectors"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    segment_number : Mapped[int] = mapped_column(unique=True)
    segment_name : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    definition : Mapped[str] = mapped_column(Text)
    key_germany_companies : Mapped[str] = mapped_column(Text)
    ai_adoption : Mapped[str] = mapped_column(String(255))
    de_market_size : Mapped[str] = mapped_column(String(100))
    regulatory_complexity : Mapped[str] = mapped_column(Text)
    platform_priority : Mapped[str] = mapped_column(String(100))
    primary_ai_entry_point : Mapped[str] = mapped_column(Text)
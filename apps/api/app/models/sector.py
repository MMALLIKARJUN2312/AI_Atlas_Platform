from sqlalchemy import String, Text 
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 
from app.models.mixins import TimestampMixin

class Sector(TimestampMixin, Base):
    __tablename__ = "sectors"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(255), index=True)
    definition : Mapped[str] = mapped_column(Text)
    key_companies : Mapped[str] = mapped_column(Text)
    ai_adoption : Mapped[str] = mapped_column(Text)
    market_size : Mapped[str] = mapped_column(Text)
    regulatory_complexity : Mapped[str] = mapped_column(Text)
    primary_ai_entry_points : Mapped[str] = mapped_column(Text)
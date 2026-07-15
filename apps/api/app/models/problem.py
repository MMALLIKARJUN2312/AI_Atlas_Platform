from sqlalchemy import Integer, String, Text 
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 
from app.models.mixins import TimestampMixin

class Problem(TimestampMixin, Base):
    __tablename__ = "problems"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    category : Mapped[str] = mapped_column(String(255))
    problem : Mapped[str] = mapped_column(Text)
    severity : Mapped[int] = mapped_column(Integer)
    ai_solution_use_case : Mapped[str] = mapped_column(Text)
    affected_companies : Mapped[str] = mapped_column(Text)
    financial_impact : Mapped[str] = mapped_column(Text)
    regulatory_triggers : Mapped[str] = mapped_column(Text)
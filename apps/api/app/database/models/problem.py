from sqlalchemy import String, Text 
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 
from app.database.models.mixins import TimestampMixin

class Problem(TimestampMixin, Base):
    __tablename__ = "problems"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    problem_id : Mapped[str] = mapped_column(String(50), unique=True, index=True)
    category : Mapped[str] = mapped_column(String(100))
    problem_statement : Mapped[str] = mapped_column(Text)
    segment_tags : Mapped[str] = mapped_column(String(100))
    vc_stage : Mapped[str] = mapped_column(String(100))
    severity : Mapped[str] = mapped_column(String(50))
    ai_use_case_solution : Mapped[str] = mapped_column(Text)
    affected_germany_companies : Mapped[str] = mapped_column(Text)
    financial_impact : Mapped[str] = mapped_column(Text)
    regulatory_trigger : Mapped[str] = mapped_column(Text)
    problem_type: Mapped[str] = mapped_column(String(100))
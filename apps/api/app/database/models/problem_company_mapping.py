from sqlalchemy import String, Text 
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base 
from app.database.models.mixins import TimestampMixin

class ProblemCompanyMapping(TimestampMixin, Base):
    __tablename__ = "problem_company_mappings"
    
    id : Mapped[int] = mapped_column(primary_key=True)
    sequence_number : Mapped[int] = mapped_column()
    problem_statement : Mapped[str] = mapped_column(Text, unique=True)
    segment_tags : Mapped[str] = mapped_column(String(100))
    vc_stage : Mapped[str] = mapped_column(String(100))
    ai_solution_1 : Mapped[str] = mapped_column(Text)
    ai_solution_2 : Mapped[str] = mapped_column(Text)
    ai_solution_3 : Mapped[str] = mapped_column(Text)
    germany_vendors : Mapped[str] = mapped_column(Text)
    roi_benchmark : Mapped[str] = mapped_column(Text)
    payback_months : Mapped[str] = mapped_column(String(100))
    regulatory_benefit : Mapped[str] = mapped_column(Text)
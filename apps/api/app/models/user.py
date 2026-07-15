from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.mixins import TimestampMixin

class User(TimestampMixin, Base):
    __tablename__ = "users" 
    
    id : Mapped[int] = mapped_column(primary_key=True)
    email : Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name : Mapped[str] = mapped_column(String(255))
    hashed_password : Mapped[str] = mapped_column(String(255))
    role : Mapped[str] = mapped_column(String(50), default="user")
    is_active : Mapped[str] = mapped_column(Boolean, default=True)
    
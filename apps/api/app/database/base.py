from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

# Import every model so Alembic discovers them.
import app.models  # noqa: E402,F401

target_metadata = Base.metadata
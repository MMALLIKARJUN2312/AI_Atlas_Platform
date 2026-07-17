from typing import Generic, TypeVar

from sqlalchemy import inspect, select, func, delete
from sqlalchemy.dialects.postgresql import insert 
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, db : AsyncSession, model : type[ModelType]):
        self.db = db 
        self.model = model
        
    async def bulk_insert(self, objects: list[ModelType]) -> int:
        self.db.add_all(objects)
        await self.db.flush()
    
        return len(objects)
    
    async def bulk_insert_ignore_conflicts(self, objects: list[ModelType], conflict_columns: list[str]) -> int:

        if not objects:
            return 0

        SKIP_COLUMNS = {"id", "created_at", "updated_at",}
        mapper = inspect(self.model)
        values = []

        for obj in objects:
            row = {}

            for column in mapper.columns:
                if column.name in SKIP_COLUMNS:
                    continue

                value = getattr(obj, column.name)

                if value is not None:
                    row[column.name] = value

            values.append(row)

        statement = insert(self.model).values(values)
        statement = statement.on_conflict_do_nothing(index_elements=conflict_columns)

        await self.db.execute(statement)
        await self.db.flush()

        return len(objects)

    async def count(self) -> int:
        result = await self.db.scalar(select(func.count()).select_from(self.model))
        
        return result or 0
    
    async def truncate(self) -> None:
        await self.db.execute(delete(self.model))
        
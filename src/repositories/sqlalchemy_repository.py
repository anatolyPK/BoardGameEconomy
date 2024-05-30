from typing import Type, TypeVar, Optional

from pydantic import BaseModel
from sqlalchemy import delete, select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from models.base import Base
from repositories.base_repository import AbstractRepository

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession):
        self._session = db_session
        self.model = model

    async def create(self, data: CreateSchemaType) -> ModelType:
        async with self._session() as session:
            print(data.dict())
            instance = self.model(**data.dict())
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(self, data: UpdateSchemaType, **filters) -> ModelType:
        async with self._session() as session:
            stmt = (
                update(self.model)
                .values(**data.dict())
                .filter_by(**filters)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def delete(self, **filters) -> None:
        async with self._session() as session:
            result = await session.execute(delete(self.model).filter_by(**filters))
            if result.rowcount == 0:
                raise NoResultFound(
                    "Нет записей, соответствующих предоставленным фильтрам."
                )
            await session.commit()

    async def get_single(self, **filters) -> Optional[ModelType] | None:
        async with self._session() as session:
            row = await session.execute(select(self.model).filter_by(**filters))
            return row.scalar_one_or_none()

    async def get_multi(
        self,
        order: str = "id",
        limit: int = 100,
        offset: int = 0,
        joinedload_type=None,
        joinedload_column=None,
        **filters,
    ) -> list[ModelType]:
        async with self._session() as session:
            stmt = select(self.model)

            if joinedload_type and joinedload_column:
                stmt = stmt.options(joinedload_type(joinedload_column))

            stmt = stmt.filter_by(**filters).order_by(order).limit(limit).offset(offset)
            row = await session.execute(stmt)
            return row.scalars().all()

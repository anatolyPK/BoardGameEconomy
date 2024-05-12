from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import joinedload, selectinload, contains_eager

from exceptions import UnauthorizedTransactionError
from models.base import GameTransaction, Game
from src.config.db.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType, UpdateSchemaType
from src.schemas.transactions import GameAddTransactionSchema, GameTransactionPatchSchema


class GameRepository(SqlAlchemyRepository[ModelType, GameAddTransactionSchema, GameTransactionPatchSchema]):
    async def get_user_transactions(
            self,
            user_id: int,
            order: str = "id",
            limit: int = 100,
            offset: int = 0,

    ) -> list[ModelType]:
        async with self._session() as session:
            stmt = select(self.model)
            stmt = stmt.join(self.model.game).join(Game.names_ru_values)
            stmt = stmt.options(contains_eager(self.model.game).contains_eager(Game.names_ru_values))
            stmt = stmt.filter(self.model.user_id == user_id).order_by(order).limit(limit).offset(offset)
            row = await session.execute(stmt)
            unique_row = row.unique().scalars().all()
            return unique_row

    async def update(self, data: UpdateSchemaType, pk: int) -> ModelType:
        async with self._session() as session:
            game_transaction = await session.get(self.model, pk)
            if not game_transaction:
                raise NoResultFound
            if game_transaction.user_id != data.user_id:
                raise UnauthorizedTransactionError
            stmt = update(self.model).values(**data.dict()).where(self.model.id == pk).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()


game_repository = GameRepository(model=GameTransaction,
                                 db_session=db_helper.get_db_session_context)

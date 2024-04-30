from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from models.base import GameTransaction, Game
from schemas.game import GameSearchSchema, GameSchema
from src.config.db.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.schemas.transactions import GameAddTransactionSchema, GameTransactionPatchSchema


class GameSearchRepository(SqlAlchemyRepository[ModelType, GameAddTransactionSchema, GameTransactionPatchSchema]):

    async def search_games(self, game_name: str) -> GameSearchSchema:
        async with self._session() as session:
            ilike_expr = self.model.name_ru.ilike(f'%{game_name.strip()}%')
            stmt = select(self.model).where(ilike_expr)
            stmt = stmt.order_by(getattr(self.model, 'name_ru')).limit(100).offset(0)
            result_orm = await session.scalars(stmt)
            result_dto = [GameSchema.model_validate(game, from_attributes=True) for game in result_orm]

            if not result_dto:
                result_dto = None

            return GameSearchSchema(games=result_dto)


game_search_repository = GameSearchRepository(model=Game,
                                              db_session=db_helper.get_db_session_context)

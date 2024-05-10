from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload

from models.base import GameTransaction, Game, GameRuName
from schemas.bggAPI_games import GameInfoSchema
from schemas.game import GameSearchSchema, GameSchema
from src.config.db.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.schemas.transactions import GameAddTransactionSchema, GameTransactionPatchSchema


class GameRepository(SqlAlchemyRepository[ModelType, GameAddTransactionSchema, GameTransactionPatchSchema]):
    async def add_game_in_db(self, games_info: list[GameInfoSchema]):
        async with self._session() as session:
            for game_info in games_info:
                stmt = select(self.model).filter(self.model.bgg_id == game_info.bgg_id)
                existing_game = await session.execute(stmt)
                if not existing_game.first():
                    game_data = game_info.dict()
                    game_data.pop('name_ru', None)
                    instance = self.model(**game_data)
                    session.add(instance)
                    await session.flush()
                    game_id = instance.id
                    await game_search_repository.create_game_name_ru(session, game_info.name_ru, game_id)
            await session.commit()

    async def get_max_bgg_id(self) -> int | None:
        async with self._session() as session:
            result = await session.execute(select(func.max(self.model.bgg_id)))
            max_bgg_id = result.scalar()
            return max_bgg_id


class GameNameRuRepository(SqlAlchemyRepository):
    async def search_games(self, game_name: str) -> GameSearchSchema:
        async with self._session() as session:
            ilike_expr = self.model.name_ru.ilike(f'%{game_name.strip()}%')
            # какую подгрузку использовать
            # включить эхо sql
            stmt = select(self.model).where(ilike_expr).options(selectinload(self.model.base_game))
            stmt = stmt.order_by(getattr(self.model, 'name_ru')).limit(100).offset(0)
            result_orm = await session.scalars(stmt)

            result_dto = []
            for game in result_orm:
                result = GameSchema(id=game.base_game.id,
                                    name_ru=game.name_ru,
                                    image=game.base_game.image,
                                    yearpublished=game.base_game.yearpublished)
                result_dto.append(result)

            return GameSearchSchema(games=result_dto)

    async def create_game_name_ru(self, session, game_ru_names: list, game_id):
        for game_ru_name in game_ru_names:
            instance = self.model(name_ru=game_ru_name, game_id=game_id)
            session.add(instance)

    # async def get_


game_downloader_repository = GameRepository(model=Game,
                                        db_session=db_helper.get_db_session_context)

game_search_repository = GameNameRuRepository(model=GameRuName,
                                               db_session=db_helper.get_db_session_context)
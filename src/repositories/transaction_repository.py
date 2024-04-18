from models.base import GameTransaction
from src.config.db.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository, ModelType
from src.schemas.transactions import GameAddTransaction, GamePatchTransaction


class GameRepository(SqlAlchemyRepository[ModelType, GameAddTransaction, GamePatchTransaction]):
    pass


game_repository = GameRepository(model=GameTransaction,
                                db_session=db_helper.get_db_session_context)

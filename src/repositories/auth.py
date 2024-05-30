from models.base import RefreshToken
from src.config.db.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository


class AuthRepository(SqlAlchemyRepository):
    pass


auth_repository = AuthRepository(
    model=RefreshToken, db_session=db_helper.get_db_session_context
)

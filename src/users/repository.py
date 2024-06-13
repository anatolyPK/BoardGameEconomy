from models.base import User
from core.config.database import db_helper
from src.repositories.sqlalchemy_repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    pass


user_repository = UserRepository(
    model=User, db_session=db_helper.get_db_session_context
)

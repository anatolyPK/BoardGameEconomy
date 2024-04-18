# from typing import Any, List, TYPE_CHECKING
#
# from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyBaseUserTableUUID
# from sqlalchemy import String, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from models.base import Base
#
#
# if TYPE_CHECKING:
#     from src.models.transactions import GameTransaction
#
#
# print('hello_m_auth')
# class User(SQLAlchemyBaseUserTableUUID, Base):
#     # __tablename__ = "user"
#
#     username: Mapped[str] = mapped_column(String(16), unique=True)
#     role_id: Mapped[int] = mapped_column(ForeignKey('role.id', ondelete='CASCADE'))
#
#     role: Mapped['Role'] = relationship(back_populates='users')
#     game_transactions: Mapped[List['GameTransaction']] = relationship(back_populates='user')
#
#
# class Role(Base):
#     __tablename__ = 'role'
#     __table_args__ = {"extend_existing": True}  # < new
#
#     name: Mapped[str] = mapped_column(String(16), unique=True)
#     permission: Mapped[dict[str, Any]] = mapped_column(nullable=True)
#
#     users: Mapped[list['User']] = relationship(back_populates='role')
#

# from typing import List, TYPE_CHECKING
#
# from sqlalchemy import ForeignKey, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from models.base import Base
#
#
# if TYPE_CHECKING:
#     from src.models.transactions import GameTransaction
#
#
# class Game(Base):
#     __tablename__ = 'game'
#
#     name: Mapped[str] = mapped_column(String(128))
#
#     games_transactions: Mapped[List['GameTransaction']] = relationship(back_populates='game')

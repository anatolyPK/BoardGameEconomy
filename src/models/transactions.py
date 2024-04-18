# from datetime import date
# from typing import TYPE_CHECKING
#
# from sqlalchemy import ForeignKey, String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from models.base import Base
#
#
# if TYPE_CHECKING:
#     from src.models.auth import User
#     from src.models.games import Game
#
#
# class GameTransaction(Base):
#     __tablename__ = 'game_transaction'
#
#     user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
#     game_id: Mapped[int] = mapped_column(ForeignKey('game.id', ondelete='CASCADE'))
#
#     purchase_date: Mapped[date]
#     purchase_price: Mapped[float]
#
#     selling_date: Mapped[date] = mapped_column(nullable=True)
#     selling_price: Mapped[float] = mapped_column(nullable=True)
#
#     description: Mapped[str] = mapped_column(String(128))
#
#     user: Mapped['User'] = relationship(back_populates='game_transactions')
#     game: Mapped['Game'] = relationship(back_populates='games_transactions')

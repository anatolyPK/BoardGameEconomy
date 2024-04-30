import uuid
from typing import Optional

from pydantic import BaseModel

from datetime import date


class BaseGameSchema(BaseModel):
    description: str
    name_en: str
    name_ru: str
    image: Optional[str] = None

    yearpublished: Optional[int] = None
    minplayers: Optional[int] = None
    maxplayers: Optional[int] = None
    playingtime: Optional[int] = None


class BaseGameTransactionSchema(BaseModel):
    purchase_date: date
    purchase_price: float

    selling_date: Optional[date] = None
    selling_price: Optional[float] = None

    description: Optional[str] = None


class GameTransactionSelectedGameSchema(BaseGameTransactionSchema):
    game: BaseGameSchema


class GameTransactionsSchema(BaseModel):
    games: Optional[list[GameTransactionSelectedGameSchema]]


class GameTransactionSchema(BaseGameTransactionSchema):
    game_id: int


class GameAddTransactionSchema(BaseGameTransactionSchema):
    game_id: int


class GameAddTransactionWithUserSchema(GameAddTransactionSchema):
    user_id: uuid.UUID


class GameTransactionPatchSchema(BaseGameTransactionSchema):
    pass


class GameTransactionPatchTransactionWithUserSchema(GameTransactionPatchSchema):
    user_id: uuid.UUID

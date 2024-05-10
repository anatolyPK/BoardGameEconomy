import uuid
from typing import Optional

from pydantic import BaseModel

from datetime import date


class GameRuName(BaseModel):
    name_ru: str


class BaseGameSchema(BaseModel):
    description: str
    names_ru_values: list[GameRuName]
    name_en: str
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

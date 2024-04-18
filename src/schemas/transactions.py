import uuid

from pydantic import BaseModel

from datetime import date


class BaseGameTransaction(BaseModel):
    game_id: int
    purchase_date: date
    purchase_price: float

    selling_date: date = None
    selling_price: float = None

    description: str = None


class GameAddTransaction(BaseGameTransaction):
    pass


class GameAddTransactionWithUser(GameAddTransaction):
    user_id: uuid.UUID


class GamePatchTransaction(BaseGameTransaction):
    pass

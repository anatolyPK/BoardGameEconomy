from pydantic import BaseModel

from schemas.transactions import BaseGameTransaction


class GeneralInfo(BaseModel):
    username: str

    game_in_stock: int
    average_price_of_game_in_stock: int
    amount_spent: int

    game_transactions: list[BaseGameTransaction]


class Stats:
    ...

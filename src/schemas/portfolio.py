from typing import Optional

from pydantic import BaseModel

from schemas.transactions import BaseGameTransactionSchema, GameTransactionSelectedGameSchema, GameTransactionsSchema


class GeneralInfoSchema(BaseModel):
    username: str

    game_in_stock: int
    average_price_of_game_in_stock: int
    amount_spent: int

    game_transactions: Optional[GameTransactionsSchema]


class ExtendedStatsSchema:
    ...

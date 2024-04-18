from models.base import User
from repositories.transaction_repository import game_repository
from schemas.transactions import GameAddTransaction, GameAddTransactionWithUser
from services.base import BaseService
from src.repositories.base_repository import AbstractRepository


class GameService(BaseService):
    def __init__(self, game_repo: AbstractRepository):
        self.game_repo: AbstractRepository = game_repo

    async def add_game(self, game: GameAddTransaction, user: User):
        game_with_user_id = GameAddTransactionWithUser(**game.dict(), user_id=user.id)
        added_game = await self.game_repo.create(game_with_user_id)
        return added_game

    # async def update_transaction(self, transaction: TransactionAdd, user: User, pk: int):
    #     transaction_with_user_id = TransactionAddWithUser(**transaction.dict(), user_id=user.id)
    #     added_transaction = await self.crypto_repo.update(transaction_with_user_id, id=pk)
    #     return added_transaction
    #
    # async def get_user_transactions(self, user: User):
    #     transactions = await self.crypto_repo.get_multi(user_id=user.id)
    #     return transactions


game_service = GameService(game_repo=game_repository)

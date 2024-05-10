from models.base import User, GameTransaction
from repositories.sqlalchemy_repository import ModelType
from repositories.transaction_repository import game_repository
from schemas.portfolio import GeneralInfoSchema
from schemas.transactions import GameAddTransactionSchema, GameAddTransactionWithUserSchema, GameTransactionPatchSchema, \
    GameTransactionPatchTransactionWithUserSchema, GameTransactionsSchema, GameTransactionSelectedGameSchema
from services.base import BaseService
from utils.users_general_info import get_users_games_general_info


class GameTransactionService(BaseService):
    async def get_users_game_info(self, user: User) -> GeneralInfoSchema:
        games = await self.get_users_board_games_transactions(user)
        general_stats = get_users_games_general_info(games, user)
        return general_stats

    async def add_game(self, game: GameAddTransactionSchema, user: User) -> ModelType:
        game_with_user_id = GameAddTransactionWithUserSchema(**game.dict(), user_id=user.id)
        added_game = await self.repository.create(game_with_user_id)
        return added_game

    async def update_transaction(self, transaction: GameTransactionPatchSchema, user: User, pk: int) -> ModelType:
        transaction_with_user_id = GameTransactionPatchTransactionWithUserSchema(**transaction.dict(), user_id=user.id)
        added_transaction = await self.repository.update(transaction_with_user_id, pk=pk)
        return added_transaction

    async def delete_transaction(self, user: User, pk: int) -> None:
        await self.repository.delete(id=pk, user_id=user.id)

    async def get_users_board_games_transactions(self, user: User) -> GameTransactionsSchema:
        result_orm = await self.repository.get_user_transactions(user_id=user.id)
        result_dto = [GameTransactionSelectedGameSchema.model_validate(game, from_attributes=True) for game in result_orm]
        return GameTransactionsSchema(games=result_dto)


game_transaction_service = GameTransactionService(repository=game_repository)

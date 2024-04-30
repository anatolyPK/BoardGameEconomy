from repositories.game import game_search_repository
from services.base import BaseService


class GameSearchService(BaseService):

    async def search_game(self, game_name: str):
        return await self.repository.search_games(game_name)


game_service = GameSearchService(repository=game_search_repository)

from repositories.game import game_search_repository, game_downloader_repository
from services.base import BaseService
from utils.bggAPI import BoardGameScraper


class GameSearchService(BaseService):
    async def search_game(self, game_name: str):
        return await self.repository.search_games(game_name)


class GameDownloaderService(BaseService):
    async def download_games(self, start: int, end: int, step: int = 100):
        if start == 0:
            start = await self.repository.get_max_bgg_id()
        if start >= end or end - start > 50000:
            raise ValueError
        games = await BoardGameScraper.scrape_games(start, end, step)
        await self.repository.add_game_in_db(games)

    async def get_max_bgg(self):
        return await self.repository.get_max_bgg_id()


game_downloader = GameDownloaderService(repository=game_downloader_repository)
game_searcher = GameSearchService(repository=game_search_repository)

import asyncio
import datetime
import aiohttp
import xml.etree.ElementTree as ET

from sqlalchemy import select

from config.db.database import db_helper
from exceptions import GamesAreOver
from models.base import Game
from schemas.bggAPI_games import GameInfoSchema


class BoardGameScraper:
    def __init__(self, db_session):
        self.db_session = db_session
        self.base_url = 'https://boardgamegeek.com/xmlapi/game/'

    async def scrape_games(self, start=363307, step=0, max_val=363308):
        async with aiohttp.ClientSession() as session:
            while start < max_val:
                end = start + step
                tasks = [self._fetch_game_info(session, number) for number in range(start, end)]
                responses = await asyncio.gather(*tasks)
                game_info = await self._process_responces(responses)
                await self._write_in_db(game_info)
                print(f'{start}, {end}')
                start += step

    async def _fetch_game_info(self, session, number):
        url = f'{self.base_url}{number}'
        async with session.get(url) as response:
            return await response.text()

    async def _process_responces(self, responses) -> list[GameInfoSchema]:
        games_info = []
        for xml in responses:
            try:
                game_info = await self.parse_game_info(xml)
                if game_info:
                    games_info.append(game_info)
            except GamesAreOver:
                pass
            except AttributeError:
                pass
        return games_info

    async def parse_game_info(self, xml) -> GameInfoSchema | None:
        if '<error message="Item not found"/>' in xml:
            raise GamesAreOver

        root = ET.fromstring(xml)
        try:
            cyrillic_names = [name.text for name in root.findall('.//name') if
                              any(cyrillic in name.text for cyrillic in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя')]
            if cyrillic_names:
                game_info = {
                    'name_en': root.find(".//name[@primary='true']").text,
                    'name_ru': cyrillic_names[0],
                    'description': root.find(".//description").text,
                    'image': root.find(".//image").text,
                    'yearpublished': root.find(".//yearpublished").text,
                    'playingtime': root.find(".//playingtime").text,
                    'minplayers': root.find(".//minplayers").text,
                    'maxplayers': root.find(".//maxplayers").text,
                }
                return GameInfoSchema(**game_info)
        except TypeError:
            return
        return

    async def _write_in_db(self, games_info):
        async with self.db_session() as session:
            for numb, game_info in enumerate(games_info):
                stmt = select(Game).filter(Game.name_ru == game_info.name_ru)
                existing_game = await session.execute(stmt)
                if not existing_game.first():
                    instance = Game(**game_info.dict())
                    session.add(instance)
            await session.commit()


async def main():
    scraper = BoardGameScraper(db_session=db_helper.get_db_session_context)
    await scraper.scrape_games()

start_time = datetime.datetime.now()
asyncio.run(main())

print(f'{datetime.datetime.now()-start_time} sec')

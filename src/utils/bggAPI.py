import asyncio
import aiohttp
import xml.etree.ElementTree as ET


from exceptions import GamesAreOver
from schemas.bggAPI_games import GameInfoSchema


class BoardGameScraper:
    base_url = "https://api.geekdo.com/xmlapi/boardgame/"

    @classmethod
    async def scrape_games(
        cls, start: int = 1, end: int = 500_000, step: int = 100
    ) -> list[GameInfoSchema]:
        print(f"{start} {end} {step}")
        async with aiohttp.ClientSession() as session:
            games_info = []
            while start < end:
                tasks = []
                for _ in range(5):
                    task = cls._fetch_game_info(session, start, step)
                    start += step
                    tasks.append(task)
                responses = await asyncio.gather(*tasks)
                games_info.extend(await cls._process_responses(responses))
            return games_info

    @classmethod
    async def _fetch_game_info(cls, session, start, step):
        print(f"START {start} STEP {step}")
        game_ids = list(range(start, start + step))
        ids_string = ",".join(str(game_id) for game_id in game_ids)
        url = f"{cls.base_url}{ids_string}"
        async with session.get(url) as response:
            return await response.text()

    @classmethod
    async def _process_responses(cls, responses) -> list[GameInfoSchema]:
        games_info = []
        for xml in responses:
            root = ET.fromstring(xml)
            for boardgame in root.findall("boardgame"):
                try:
                    game_info = await cls.parse_game_info(boardgame)
                    if game_info:
                        games_info.append(game_info)
                except GamesAreOver:
                    pass
                except AttributeError:
                    pass
        return games_info

    @classmethod
    async def parse_game_info(cls, boardgame) -> GameInfoSchema | None:
        if '<error message="Item not found"/>' in boardgame:
            raise GamesAreOver
        try:
            cyrillic_names = [
                name.text
                for name in boardgame.findall(".//name")
                if any(
                    cyrillic in name.text
                    for cyrillic in "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                )
                and all(
                    ukrainan.lower() not in name.text.lower() for ukrainan in "ҐЄІЇЇ̈"
                )
            ]
            if cyrillic_names:
                return GameInfoSchema(
                    bgg_id=int(boardgame.attrib.get("objectid")),
                    name_en=boardgame.find(".//name[@primary='true']").text,
                    name_ru=cyrillic_names,
                    description=boardgame.find(".//description").text,
                    image=boardgame.find(".//image").text,
                    yearpublished=boardgame.find(".//yearpublished").text,
                    playingtime=boardgame.find(".//playingtime").text,
                    minplayers=boardgame.find(".//minplayers").text,
                    maxplayers=boardgame.find(".//maxplayers").text,
                )
        except TypeError:
            return


# async def main():
#     await BoardGameScraper.scrape_games(0, 100)
#
# if __name__ == '__main__':
#
#     start_time = datetime.datetime.now()
#     asyncio.run(main())
#
#     print(f'{datetime.datetime.now()-start_time} sec')

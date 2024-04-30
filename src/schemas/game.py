from typing import Optional

from pydantic import BaseModel


class GameSchema(BaseModel):
    id: int
    name_ru: str
    image: Optional[str] = None
    yearpublished: Optional[int]


class GameSearchSchema(BaseModel):
    games: Optional[list[GameSchema]]


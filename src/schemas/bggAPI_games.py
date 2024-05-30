from typing import Optional

from pydantic import BaseModel, field_validator


class GameInfoSchema(BaseModel):
    bgg_id: int
    name_en: str
    name_ru: list[str]
    description: str
    image: Optional[str]

    yearpublished: Optional[int] = None
    playingtime: Optional[int] = None
    minplayers: Optional[int] = None
    maxplayers: Optional[int] = None

    @field_validator("description")
    @classmethod
    def validate_description_length(cls, v):
        return cls.cut_string(v, 2048)

    @field_validator("name_en")
    @classmethod
    def validate_name_en_length(cls, v):
        return cls.cut_string(v, 128)

    @field_validator("name_ru")
    @classmethod
    def validate_name_ru_length(cls, v):
        for numb in range(len(v)):
            v[numb] = cls.cut_string(v[numb], 128)
        return v

    @field_validator("yearpublished")
    @classmethod
    def validate_yearpublished_int(cls, v):
        return cls.int_maker(v)

    @field_validator("playingtime")
    @classmethod
    def validate_playingtime_int(cls, v):
        return cls.int_maker(v)

    @field_validator("minplayers")
    @classmethod
    def validate_minplayers_int(cls, v):
        return cls.int_maker(v)

    @field_validator("maxplayers")
    @classmethod
    def validate_maxplayers_int(cls, v):
        return cls.int_maker(v)

    @classmethod
    def int_maker(cls, value):
        try:
            return int(value)
        except TypeError:
            return None

    @classmethod
    def cut_string(cls, string: str, end: int):
        if len(string) > end:
            return string[:end]
        return string

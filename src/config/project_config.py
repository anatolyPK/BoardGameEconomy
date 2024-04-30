import dotenv
from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()
print('ПЕРЕМЕННЫЕ!!!!')
print(dotenv.dotenv_values())

class Settings(BaseSettings):
    DB_ECHO: bool
    PROJECT_NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str


settings = Settings()

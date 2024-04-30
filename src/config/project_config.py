import os

from dotenv import load_dotenv

from pydantic_settings import BaseSettings


load_dotenv()


db_echo = os.environ['DB_ECHO']
project_name = os.environ['PROJECT_NAME']
version = os.environ['VERSION']
debug = os.environ['DEBUG']
cors = os.environ['CORS_ALLOWED_ORIGINS']


class Settings(BaseSettings):
    DB_ECHO: bool = db_echo
    PROJECT_NAME: str = project_name
    VERSION: str = version
    DEBUG: bool = debug
    CORS_ALLOWED_ORIGINS: str = cors


settings = Settings()

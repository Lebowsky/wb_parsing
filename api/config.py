from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

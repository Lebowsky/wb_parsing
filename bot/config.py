from pydantic_settings import BaseSettings
from pydantic import HttpUrl


class Settings(BaseSettings):
    token: str
    admins_id: list[int]
    server_url: HttpUrl


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

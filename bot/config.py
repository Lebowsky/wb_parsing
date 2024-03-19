from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    token: str
    admins_id: list[int]
    server_url: str


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')

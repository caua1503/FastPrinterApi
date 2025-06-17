import os

from pydantic_settings import BaseSettings, SettingsConfigDict

caminho = os.path.dirname(os.path.abspath(__file__))


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(caminho, ".env"), env_file_encoding="utf-8")

    REDIS_HOST: str
    REDIS_PORT: str
    DATABASE_URL: str

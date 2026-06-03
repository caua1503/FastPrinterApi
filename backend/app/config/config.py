from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int
    DATABASE_URL: str

    JWT_ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    PRINTER_MAINTENANCE_BATCH_SIZE: int


@lru_cache
def get_config() -> Config:
    return Config()

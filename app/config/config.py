from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    REDIS_HOST: str
    REDIS_PORT: str
    DATABASE_URL: str
    JWT_ALGORITHM: str

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_DB: int
    REDIS_URL: str
    DATABASE_URL: str
    DATABASE_LOGS_URL: str
    JWT_ALGORITHM: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

from functools import lru_cache
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.core.path import ROOT_PATH
# Get the settings from the .env file
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    db_host: str
    db_port: int
    db_user: str
    db_password: SecretStr
    db_name: str
    redis_host: str
    redis_port: int

@lru_cache
def get_settings() -> Settings:
    # Avoid creating multiple instances of Settings by caching the result
    return Settings()
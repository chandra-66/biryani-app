from functools import lru_cache
from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Biryani App Backend"
    app_env: str = "development"
    database_url: str = "sqlite:///./biryani_app.db"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expires_minutes: int = 60
    jwt_refresh_token_expires_days: int = 7
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    simulated_payment_mode: bool = True

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=False,
        env_prefix=''
    )

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(',') if origin.strip()]

    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value:
            raise ValueError('database_url cannot be empty')
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()

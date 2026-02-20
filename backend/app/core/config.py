from functools import lru_cache
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    project_name: str = "codex-app-boilerplate"
    environment: Literal["development", "staging", "production"] = "development"
    backend_cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    database_url: str = "postgresql+psycopg://app_user:app_password@db:5432/app_db"

    redis_url: str = "redis://redis:6379/0"
    llm_cache_enabled: bool = True
    openai_cache_ttl_seconds: int = 3600
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    prompts_dir: Path = Path("/app/prompts")

    auth_enabled: bool = False
    auth0_domain: str | None = None
    auth0_audience: str | None = None
    auth0_issuer: str | None = None

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        raise ValueError("BACKEND_CORS_ORIGINS must be a comma-separated string or list")

    @field_validator("auth0_domain", mode="before")
    @classmethod
    def normalize_auth0_domain(cls, value: str | None) -> str | None:
        if not value:
            return value
        return value.replace("https://", "").replace("http://", "").rstrip("/")

    @model_validator(mode="after")
    def populate_auth0_defaults(self) -> "Settings":
        if self.auth0_domain and not self.auth0_issuer:
            self.auth0_issuer = f"https://{self.auth0_domain.rstrip('/')}/"
        elif self.auth0_issuer:
            self.auth0_issuer = self.auth0_issuer.rstrip("/") + "/"
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()

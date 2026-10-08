"""Application configuration.

Reads environment variables (see root ``.env.example``). The AI provider is
selected here: by default ShopDoctor runs fully offline with the ``mock``
provider. Set ``LLM_PROVIDER=openai`` (or ``anthropic``) plus an API key to
switch to real model calls without touching any other code.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "ShopDoctor API"
    version: str = "0.1.0"
    environment: str = "development"

    # Database
    database_url: str = "sqlite:///./shopdoctor.db"

    # CORS (frontend dev server)
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # AI layer -------------------------------------------------------------
    # "mock" -> deterministic offline agents (default, no key needed)
    # "openai" / "anthropic" -> real-ready provider (requires api key)
    llm_provider: str = "mock"
    llm_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    llm_timeout: float = 30.0

    # Pricing model
    default_elasticity: float = -1.4

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

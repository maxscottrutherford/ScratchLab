from functools import lru_cache

from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Server-side settings. Never load SUPABASE_PUBLISHABLE_KEY here — backend uses the secret key only."""

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "ScratchLab API"
    app_version: str = "0.1.0"

    supabase_url: HttpUrl = Field(description="Supabase project URL")
    supabase_secret_key: str = Field(
        description="Supabase service_role key; bypasses RLS. Never send to clients.",
    )

    openai_api_key: str | None = None
    golf_course_api_key: str | None = None
    google_places_api_key: str | None = None

    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated browser origins allowed by CORS",
    )
    cors_origin_regex: str | None = Field(
        default=r"https://.*\.vercel\.app",
        description="Regex for additional origins (e.g. Vercel preview/production)",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    """Read configuration from environment (load `.env` in `main.py` before importing routers)."""
    return Settings()

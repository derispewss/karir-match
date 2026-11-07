"""Konfigurasi aplikasi dari environment lokal."""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


def _csv_env(name: str, default: str) -> tuple[str, ...]:
    """Baca daftar yang dipisahkan koma dari environment."""
    raw = os.getenv(name, default)
    return tuple(item.strip() for item in raw.split(",") if item.strip())


@dataclass(frozen=True)
class Settings:
    """Nilai konfigurasi yang dibaca sekali saat modul diimpor."""

    app_name: str = "KarirMatch API"
    app_env: str = os.getenv("APP_ENV", "development")
    secret_key: str = os.getenv("SECRET_KEY", "dev-only-change-me")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./karirmatch.db")
    cors_origins: tuple[str, ...] = field(
        default_factory=lambda: _csv_env(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173",
        )
    )
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()

"""Entry point API KarirMatch.

Fase 0 hanya menyediakan health check untuk memverifikasi environment.
Endpoint produk akan ditambahkan pada fase berikutnya.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

APP_VERSION = "0.1.0"

app = FastAPI(
    title=settings.app_name,
    version=APP_VERSION,
    description="API pencarian dan rekomendasi lowongan kerja KarirMatch.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Health check untuk memastikan aplikasi dan konfigurasi dasar berjalan."""
    return {
        "status": "ok",
        "service": "karirmatch-api",
        "version": APP_VERSION,
        "environment": settings.app_env,
    }


@app.get("/", include_in_schema=False)
def root() -> dict[str, str]:
    """Arahkan pengguna ke dokumentasi dan health check."""
    return {
        "name": settings.app_name,
        "docs": "/docs",
        "health": "/health",
    }

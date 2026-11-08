"""Entry point API KarirMatch – Phase 6 MVP."""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# Import routers (backend MVP)
from app.routers import (
    admin,
    auth,
    bookmarks,
    events,
    jobs,
    preferences,
    recommendations,
    user,
)

APP_VERSION = "0.1.0"

app = FastAPI(
    title=settings.app_name,
    version=APP_VERSION,
    description="API pencarian dan rekomendasi lowongan kerja KarirMatch.",
)

# CORS – allow configured origins (dev: *).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add baseline security headers to every response."""
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    )
    response.headers["Strict-Transport-Security"] = (
        "max-age=15768000; includeSubDomains; preload"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    return response


# Include all routers
app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(preferences.router)
app.include_router(bookmarks.router)
app.include_router(events.router)
app.include_router(recommendations.router)
app.include_router(admin.router)
app.include_router(user.router)


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

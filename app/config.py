"""Application configuration using Pydantic BaseSettings.

In production load values from environment variables or a .env file.
For this MVP we expose a minimal set: app name, environment, and CORS origins.
`CORS_ORIGINS` uses a comma-separated string so it can be set directly in
Docker Compose without JSON escaping.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "KarirMatch API"
    app_env: str = "development"
    cors_origins: str = "*"

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse comma-separated origins into a list."""
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


settings = Settings()

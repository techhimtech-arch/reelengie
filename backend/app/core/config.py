from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REELENGINE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    host: str = "127.0.0.1"
    port: int = 8765
    projects_dir: str = "projects"
    log_level: str = "INFO"
    app_name: str = "Reel Engine"
    app_version: str = "0.1.0"

    @property
    def cors_origins(self) -> list[str]:
        return [
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "file://",
        ]


settings = Settings()

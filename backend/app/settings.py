from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Kouzina Reco API"
    environment: str = "local"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/kouzina_reco"
    allowed_origins: str = (
        "http://localhost:3000,"
        "http://localhost:5500,"
        "http://localhost:5600,"
        "http://localhost:8000,"
        "https://www.kouzinaclub.com.br,"
        "https://kouzinaclub.com.br"
    )
    public_widget_key: str = "kouzina_public_dev_key"

    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def allowed_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()

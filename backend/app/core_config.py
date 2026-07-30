from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Trade AI"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://trade_ai:trade_ai_password@localhost:5432/trade_ai"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()

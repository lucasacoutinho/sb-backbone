from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Use standard Python type hints + Field defaults.
    APP_URL: str = Field(default="http://localhost")

    API_SECRET: str = Field(default="change-me")
    PORT: int = Field(default=42069)

    DB_HOST: str = Field(default="ms-auth-db")
    DB_PORT: int = Field(default=5432)
    DB_USER: str = Field(default="ms-auth-db")
    DB_PASS: str = Field(default="ms-auth-db")
    DB_DATABASE: str = Field(default="ms-auth-db")

    OPEN_AI_URL: str = Field(default="change-me")
    OPEN_AI_KEY: str = Field(default="change-me")

    # Pydantic 2.x: specify env_file in the model config
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


settings = Settings()

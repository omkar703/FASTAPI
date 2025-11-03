from pydantic_settings import BaseSettings , SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL : str
    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra='ignore'
    )

Config = Settings()

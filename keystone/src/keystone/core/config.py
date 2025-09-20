from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./keystone.db"
settings = Settings()

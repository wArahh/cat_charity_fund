from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str

    class Config:
        env_file = '.env'


settings = Settings()

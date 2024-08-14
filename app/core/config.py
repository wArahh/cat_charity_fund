from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str = 'Кошачий благотворительный фонд (0.1.0)'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'

    class Config:
        env_file = '.env'


settings = Settings()

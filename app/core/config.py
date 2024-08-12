from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str
    database_url: str

    class Config:
        env_file = '.env'


settings = Settings()

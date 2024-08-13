from pydantic import BaseSettings


class Settings(BaseSettings):
    title: str
    database_url: str
    secret: str

    class Config:
        env_file = '.env'


settings = Settings()

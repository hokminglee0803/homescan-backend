from pydantic import BaseSettings, Field
from functools import lru_cache


class Settings(BaseSettings):
    name: str = Field(..., env="PROJ_NAME")
    mongodb_connection_string: str = Field(...,
                                           env='MONGODB_CONNECTION_STRING')
    redis_url: str = Field(..., env="REDIS_URL")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()

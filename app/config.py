from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str
    HOST: str
    DEBUG_MODE: str
    PORT: int
    URLS: List[str] = [
        "https://api1.com/?member_id={}",
        "https://api2.com/?member_id={}",
        "https://api3.com/?member_id={}",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

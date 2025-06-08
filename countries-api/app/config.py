# app/config.py
import os

from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Countries API"
    PROJECT_DESCRIPTION: str = "An API for country data"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/v1"
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")

    class Config:
        env_file = ".env"

settings = Settings()
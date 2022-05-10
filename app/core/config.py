import os
from typing import List

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings, AnyHttpUrl, EmailStr

load_dotenv()


class CommonSettings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME")
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY")


class ServerSettings(BaseSettings):
    HOST: AnyHttpUrl = "http://localhost:8000"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8000", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []


class DatabaseSettings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DB_NAME: str = os.getenv("DB_NAME")


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    SECURE_COOKIE: bool = False
    # Google authentication
    GOOGLE_OAUTH_CLIENT_ID: str = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET: str = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")


class MailSettings(BaseSettings):
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY")


class AdminSettings(BaseSettings):
    FIRST_SUPERUSER: EmailStr = os.getenv("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD")
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


class Settings(CommonSettings, ServerSettings, DatabaseSettings, AuthSettings, MailSettings, AdminSettings):
    pass


settings = Settings()

client = AsyncIOMotorClient(settings.MONGODB_URL + settings.DB_NAME, uuidRepresentation="standard")
db = client.get_default_database()

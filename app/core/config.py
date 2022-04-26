from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseSettings


class CommonSettings(BaseSettings):
    APP_NAME: str = "FastAPI + MongoDB"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str


class AuthSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    SECURE_COOKIE: bool = False


class Settings(CommonSettings, ServerSettings, DatabaseSettings, AuthSettings):
    pass


settings = Settings()

client = AsyncIOMotorClient(settings.MONGO_URI, uuidRepresentation="standard")

db = client.get_default_database()

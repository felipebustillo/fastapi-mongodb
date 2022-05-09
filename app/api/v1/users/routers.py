from fastapi import APIRouter

from app.core.config import settings
from .auth import auth_backend, fastapi_users, google_oauth_client
from .models import UserCreate, UserRead, UserUpdate

users_router = APIRouter()

users_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

users_router.include_router(
    fastapi_users.get_oauth_router(google_oauth_client, auth_backend, settings.SECRET_KEY),
    prefix="/auth/google",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

users_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

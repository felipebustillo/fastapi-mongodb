from fastapi import APIRouter

from auth import auth_backend, fastapi_users

users_router = APIRouter(
    prefix="/api/v1"
)


def get_users_router():
    users_router.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
    users_router.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
    users_router.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
    users_router.include_router(fastapi_users.get_verify_router(), prefix="/auth", tags=["auth"])
    users_router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

    return users_router

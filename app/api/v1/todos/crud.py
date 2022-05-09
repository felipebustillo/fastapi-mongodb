from fastapi import Depends

from app.api.v1.users.auth import current_active_verified_user
from app.api.v1.users.models import User


async def get_todos(user: User = Depends(current_active_verified_user)):
    return f"Hello, {user.email}"


async def get_todo(user: User = Depends(current_active_verified_user)):
    return f"Hello, {user.email}"



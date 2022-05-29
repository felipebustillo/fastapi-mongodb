from beanie import PydanticObjectId
from fastapi import HTTPException
from pydantic import EmailStr

from app.api.v1.users.models import User


async def get_user_by_id(id: PydanticObjectId) -> User:
    user = await User.get(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_user_by_email(email: EmailStr) -> User:
    user = await User.by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

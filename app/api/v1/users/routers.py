from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Response, HTTPException

from app.api.v1.auth.mail import send_verification_email
from app.api.v1.users.models import User
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def create_user(user: User):
    _user = await User.by_email(user.email)
    if _user is not None:
        raise HTTPException(
            status_code=409,
            detail="An user with that email already exists"
        )
    user.password = get_password_hash(user.password)
    await user.insert()
    if user.is_verified is False:
        await send_verification_email(user)
    return Response(
        status_code=201,
        content="User created"
    )


@router.get("", response_model=List[User])
async def get_users():
    return await User.find_all().to_list()


@router.get("/{id}", response_model=User)
async def get_user(id: PydanticObjectId):
    user = await get_user_by_id(id)
    return user


@router.put("/{id}", response_model=User)
async def update_user(id: PydanticObjectId, update: User):
    user = await get_user_by_id(id)
    user.copy()
    await user.save()
    return user


@router.delete("/{id}")
async def delete_user(id: PydanticObjectId):
    user = await get_user_by_id(id)
    await user.delete()
    return Response(
        status_code=200,
        content="User deleted"
    )


async def get_user_by_id(id: PydanticObjectId) -> User:
    user = await User.get(id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Response, Depends, Body, HTTPException

from app.api.v1.auth.mail import send_verification_email
from app.api.v1.auth.oauth import get_current_verified_user
from app.api.v1.users.models import User, UserUpdate, UserLogin
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("")
async def create_user(user: User = Body(...)):
    user_ = await User.find_one(User.email == user.email)
    if user_:
        raise HTTPException(status_code=409, detail="An user with that email already exists")
    user.hashed_password = get_password_hash(user.hashed_password)
    await user.create()
    if user.is_verified is False:
        await send_verification_email(user)
    return Response(status_code=201, content="User created")


@router.get("", response_model=List[User])
async def get_users():
    return await User.find_all().to_list()


@router.get("/{id}", response_model=User)
async def get_user(id: PydanticObjectId):
    user = await User.find_one(User.id == id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/me", response_model=User)
async def get_current_user(user: User = Depends(get_current_verified_user)):
    return user.email + "authenticated"


@router.put("/{id}", response_model=User)
async def update_user(id: PydanticObjectId, user_update: UserUpdate = Body(...)):
    user = await User.find_one(User.id == id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)
        await user.save()
    user_update = {k: v for k, v in user_update.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in user_update.items()
    }}
    await user.update(update_query)
    return user


@router.put("/me", response_model=User)
async def update_current_user(id: PydanticObjectId, current_user: User = Depends(get_current_verified_user)):
    user = await User.find_one(User.id == id)
    user.copy()
    await user.save()
    return user


@router.delete("/{id}")
async def delete_user(id: PydanticObjectId):
    user = await User.find_one(User.id == id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return Response(status_code=200, content="User deleted")

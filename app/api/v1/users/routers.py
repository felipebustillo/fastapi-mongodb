from datetime import datetime
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, Response, Body, HTTPException, Depends

from app.api.v1.auth.mail import send_verification_email
from app.api.v1.auth.oauth import get_current_verified_user, get_current_admin
from app.api.v1.users.models import User, UserUpdate, UserOut, UserUpdateCurrent
from app.core.security import get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("", dependencies=[Depends(get_current_admin)])
async def create_user(user: User):
    user_ = await User.find_one(User.email == user.email)
    if user_:
        raise HTTPException(status_code=409, detail="An user with that email already exists")
    user.hashed_password = get_password_hash(user.hashed_password)
    await user.create()
    if user.is_verified is False:
        await send_verification_email(user)
    return Response(status_code=201, content="User created")


@router.get("", response_model=List[User], dependencies=[Depends(get_current_admin)])
async def get_users():
    return await User.find_all().to_list()


@router.get("/current")
async def get_current_user(current_user: User = Depends(get_current_verified_user)):
    user = UserOut(
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email
    )
    return user


@router.get("/{user_id}", response_model=User, dependencies=[Depends(get_current_admin)])
async def get_user(user_id: PydanticObjectId):
    user = await User.find_one(User.id == user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/current", response_model=User)
async def update_user(user_update: UserUpdateCurrent = Body(...), current_user: User = Depends(get_current_verified_user)):
    user = await User.find_one(User.id == current_user.id)
    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)
        await user.save()
    user_update = {k: v for k, v in user_update.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in user_update.items()
    }}
    user.updated = datetime.utcnow()
    await user.update(update_query)
    return user


@router.put("/{user_id}", response_model=User, dependencies=[Depends(get_current_admin)])
async def update_user(user_id: PydanticObjectId, user_update: UserUpdate = Body(...)):
    user = await User.find_one(User.id == user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)
        await user.save()
    user_update = {k: v for k, v in user_update.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in user_update.items()
    }}
    user.updated = datetime.utcnow()
    await user.update(update_query)
    return user


@router.delete("/{user_id}", dependencies=[Depends(get_current_admin)])
async def delete_user(user_id: PydanticObjectId):
    user = await User.find_one(User.id == user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    return Response(status_code=200, content="User deleted")

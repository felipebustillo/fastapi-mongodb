from fastapi import APIRouter

from app.api.v1.users.models import User, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/register")
async def register(user: UserCreate):
    user = await User.email
    return "hello"


@router.post("/login")
async def login(user: UserCreate):
    user = await User.email
    return user

from fastapi import APIRouter

from app.api.v1.users.models import User

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("")
async def create_user(user: User):
    user.email = 'lol'
    return user

from typing import List

from beanie import PydanticObjectId
from fastapi_users import schemas
from fastapi_users.db import BaseOAuthAccount, BeanieBaseUser, BeanieUserDatabase
from pydantic import Field


class OAuthAccount(BaseOAuthAccount):
    pass


class User(BeanieBaseUser[PydanticObjectId]):
    oauth_accounts: List[OAuthAccount] = Field(default_factory=list)
    pass


class UserRead(schemas.BaseUser[PydanticObjectId]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


async def get_user_db():
    yield BeanieUserDatabase(User)

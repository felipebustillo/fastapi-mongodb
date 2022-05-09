from fastapi import APIRouter

from app.api.v1.todos.crud import get_todos

todos_router = APIRouter()

todos_router.include_router(
    get_todos()
)

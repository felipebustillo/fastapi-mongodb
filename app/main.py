from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.users import routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.get_users_router())

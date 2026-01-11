# from typing import Union
from fastapi import FastAPI
from src.infrastructure.adapters.routes import item_routes, user_routes

app = FastAPI()

app.include_router(user_routes.router)
app.include_router(item_routes.router)
# from typing import Union
from fastapi import FastAPI
from src.infrastructure.adapters.input.routes import item_routes, user_routes

app = FastAPI()

app.include_router(user_routes.router)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
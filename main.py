# from typing import Union
from fastapi import FastAPI
from src.infrastructure.adapters.routes import item_routes, user_routes, auction_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://crownandtrade.com",
        "https://www.crownandtrade.com",
        "http://localhost:8100",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(item_routes.router)
app.include_router(auction_routes.router)
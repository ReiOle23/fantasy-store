# from typing import Union
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.adapters.routes import item_routes, user_routes, auction_routes
from src.infrastructure.scheduler import auction_refresh_loop
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(auction_refresh_loop())
    try:
        yield
    finally:
        task.cancel()


app = FastAPI(lifespan=lifespan)

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
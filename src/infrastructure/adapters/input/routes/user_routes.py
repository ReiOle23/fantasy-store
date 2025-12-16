
from fastapi import APIRouter
from src.infrastructure.adapters.input.controllers.user_controller import UserController

router = APIRouter()

@router.get("/register-user", tags=["users"])
async def register_user(name:str, password:str) -> dict:
    new_user = UserController().create_user(name,password)
    return new_user

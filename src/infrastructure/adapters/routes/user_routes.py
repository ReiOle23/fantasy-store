from fastapi import APIRouter, status
from src.infrastructure.adapters.schemas.user import RegisterUserRequest, UserResponse, UserTokenRequest
from src.infrastructure.adapters.controllers.user_controller import UserController

router = APIRouter()

@router.post("/register-user", tags=["users"], response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(payload: RegisterUserRequest) -> UserResponse:
	return await UserController().create_user(payload)

@router.post("/login-user", tags=["users"], response_model=UserResponse, status_code=status.HTTP_200_OK)
async def login_user(payload: RegisterUserRequest) -> UserResponse:
	return await UserController().login_user(payload)

@router.patch("/user-add-money", tags=["users"], response_model=UserResponse, status_code=status.HTTP_200_OK)
async def add_money(payload: UserTokenRequest) -> UserResponse:
	return await UserController().add_money(payload)

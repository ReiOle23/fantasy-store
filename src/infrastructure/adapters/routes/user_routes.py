from fastapi import APIRouter, status
from src.infrastructure.adapters.schemas.user import RegisterUserRequest, UserResponse
from src.infrastructure.adapters.controllers.user_controller import UserController

router = APIRouter()

@router.post("/register-user", tags=["users"], response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegisterUserRequest) -> UserResponse:
	# if _repo.find_by_name(payload.name):
	# 	raise HTTPException(status_code=400, detail="user already exists")
	return UserController().create_user(payload)

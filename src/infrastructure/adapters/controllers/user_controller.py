from src.infrastructure.adapters.schemas.user import RegisterUserRequest, UserResponse
from src.application.adapters.user_service import UserService

class UserController:
    def __init__(self):
        self.use_case = UserService()

    async def create_user(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.execute(name=payload.name, password=payload.password)
        return UserResponse(id=user["id"], name=user["name"])

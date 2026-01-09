from src.infrastructure.adapters.schemas.user import RegisterUserRequest, UserResponse
from src.application.adapters.user_service import UserService

class UserController:
    def __init__(self):
        self.use_case = UserService()

    async def create_user(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.create(name=payload.name, password=payload.password)
        return UserResponse(
            id=user.id, 
            name=user.name, 
            token=user.token, 
            items=user.items, 
            money=user.money
            )
        
    async def login_user(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.login(name=payload.name, password=payload.password)
        return UserResponse(
            id=user.id, 
            name=user.name, 
            token=user.token, 
            items=user.items, 
            money=user.money
            )

    async def add_money(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.add_money(user_id=payload.id, token=payload.token, amount=payload.amount)
        return UserResponse(
            id=user.id, 
            name=user.name, 
            token=user.token, 
            items=user.items, 
            money=user.money
            )
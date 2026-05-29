from src.infrastructure.adapters.schemas.user import RegisterUserRequest, UserResponse
from src.infrastructure.adapters.schemas.item import ItemObject
from src.application.adapters.user_service import UserService

class UserController:
    def __init__(self):
        self.use_case = UserService()
        
    def _return_user_response(self, user) -> UserResponse:
        return UserResponse(
            id=user.id, 
            name=user.name, 
            token=user.token, 
            items=[
                ItemObject(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity,
                    price=item.price,
                    owner=item.owner,
                    properties=item.properties
                )
                for item in user.items
            ],
            money=user.money
            )

    async def create_user(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.create(name=payload.name, password=payload.password)
        return self._return_user_response(user)
        
    async def login_user(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.login(name=payload.name, password=payload.password)
        return self._return_user_response(user)

    async def add_money(self, payload: RegisterUserRequest) -> UserResponse:
        user = await self.use_case.add_money(user_id=payload.id, token=payload.token, amount=payload.amount)
        return self._return_user_response(user)

    async def add_item(self, payload) -> ItemObject:
        item = await self.use_case.add_item(
            user_id=payload.user_id,
            token=payload.user_token,
            name=payload.name,
            price=payload.price,
            quantity=payload.quantity,
            item_type=payload.item_type,
            properties=payload.properties,
        )
        return ItemObject(
            id=item.id,
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            owner=item.owner,
            item_type=item.item_type,
            properties=item.properties,
        )
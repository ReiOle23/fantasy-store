from src.domain.entities.user import User
from src.domain.entities.item import Item
from src.infrastructure.database import MongoDB
from src.application.ports.repositories.user_repository import UserRepository
import hashlib
from fastapi import HTTPException, status

class UserService(UserRepository):
    def __init__(self):
        self.db = MongoDB
        
    def _encode_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    async def _save_user(self, *args, **kwargs) -> User:
        new_user = User(*args, **kwargs)
        await self.db.save_obj(new_user)
        return new_user
    
    async def create(self, name: str, password: str) -> User:
        if await self.db.find_by_field(User, "name", name):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user already exists")
        
        password_hash = self._encode_password(password)
        return await self._save_user(name, password_hash)

    async def login(self, name: str, password: str) -> User:
        user_exists = await self.db.find_by_field(User, "name", name)
        password_hash = self._encode_password(password)
        if user_exists and user_exists.password == password_hash:
            return user_exists
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    
    def _check_valid_user(self, user_obj: User, user_token: str):
        if user_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user_obj.token != user_token:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid user token")

    async def add_money(self, user_id: str, token: str, amount: int) -> User:
        user_obj = await self.db.get_obj(User, user_id)
        self._check_valid_user(user_obj, token)

        user_obj.money += amount
        await self.db.save_obj(user_obj)
        return user_obj

    async def set_name(self, user_id: str, token: str, name: str) -> User:
        user_obj = await self.db.get_obj(User, user_id)
        self._check_valid_user(user_obj, token)

        if user_obj.name != name:
            existing = await self.db.find_by_field(User, "name", name)
            if existing and existing.id != user_id:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name already taken")
            user_obj.name = name
            await self.db.save_obj(user_obj)
        return user_obj

    async def add_item(self, user_id: str, token: str, name: str, price: int,
                       quantity: int, item_type: str, properties: dict) -> Item:
        user_obj = await self.db.get_obj(User, user_id)
        self._check_valid_user(user_obj, token)

        item = Item(
            name=name,
            price=price,
            quantity=quantity,
            owner=user_id,
            item_type=item_type,
            properties=properties or {},
        )
        user_obj.add_item(item)
        await self.db.save_obj(user_obj)
        return item
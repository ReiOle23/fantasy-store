from src.domain.entities.user import User
from src.infrastructure.database import MongoDB
from src.application.ports.repositories.user_repository import UserRepository
import hashlib

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
            raise Exception("user already exists")
        
        password_hash = self._encode_password(password)
        return await self._save_user(name, password_hash)

    async def login(self, name: str, password: str) -> User:
        user_exists = await self.db.find_by_field(User, "name", name)
        password_hash = self._encode_password(password)
        if user_exists and user_exists.password == password_hash:
            return user_exists
        raise Exception("Invalid credentials")
    
    def _check_valid_user(self, user_obj: User, user_token: str):
        if user_obj is None:
            raise Exception("User not found")
        if user_obj.token != user_token:
            raise Exception("Invalid user token")
    
    async def add_money(self, user_id: str, token: str, amount: int) -> User:
        user_obj = await self.db.get_obj(User, user_id)
        self._check_valid_user(user_obj, token)
        
        user_obj.money += amount
        await self.db.save_obj(user_obj)
        return user_obj
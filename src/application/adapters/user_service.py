from src.domain.entities.user import User
from src.infrastructure.database import Database
from src.application.ports.repositories.user_repository import UserRepository

import hashlib

class UserService(UserRepository):
    def __init__(self):
        self.db = Database
        
    def _encode_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    def _save_user(self, *args, **kwargs) -> User:
        new_user = User(*args, **kwargs)
        self.db.save_obj(new_user)
        return new_user

    def create(self, name: str, password: str) -> User:
        if self.db.find_by_field(User, "name", name):
            raise ValueError("user already exists")
        
        password_hash = self._encode_password(password)
        return self._save_user(name, password_hash)

    def login(self, name: str, password: str) -> User:
        user_exists = self.db.find_by_field(User, "name", name)
        password_hash = self._encode_password(password)
        if user_exists and user_exists.password == password_hash:
            return user_exists
        raise ValueError("Invalid credentials")
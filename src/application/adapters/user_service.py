from src.domain.entities.user import User
from src.infrastructure.database import Database
import hashlib
from src.application.ports.repositories.user_repository import UserRepository
from dataclasses import asdict

class UserService(UserRepository):
    def __init__(self):
        self.db = Database
        
    def _encode_password(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    def _save_user(self, *args, **kwargs) -> dict:
        new_user = User(*args, **kwargs)
        self.db.save_obj(new_user)
        return asdict(new_user)

    def create(self, name: str, password: str) -> dict:
        if self.db.find_by_field("User", "name", name):
            raise ValueError("user already exists")
        
        password_hash = self._encode_password(password)
        return self._save_user(name, password_hash)

    def login(self, name: str, password: str) -> dict:
        user_exists = self.db.find_by_field("User", "name", name)
        if user_exists:
            password_hash = self._encode_password(password)
            if user_exists["password"] == password_hash:
                return user_exists
        raise ValueError("Invalid credentials")
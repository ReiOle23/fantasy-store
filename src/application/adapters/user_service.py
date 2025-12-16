from src.domain.entities.user import User
from src.infrastructure.database import Database
import uuid, hashlib
from src.application.ports.repositories.user_repository import UserRepository

class RegisterUserUseCase(UserRepository):
    def __init__(self):
        self.db = Database

    def execute(self, name: str, password: str) -> dict:
        # check uniqueness by name
        if self.db.find_by_field("User", "name", name):
            raise ValueError("user already exists")
        # create user and persist
        new_id = str(uuid.uuid4())
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        new_user = User(id=new_id, name=name, password=password_hash)
        self.db.save_obj(new_user)
        return {"id": new_user.id, "name": new_user.name}

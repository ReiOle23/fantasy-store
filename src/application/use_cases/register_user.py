from src.domain.repositories.user_repository import UserRepository
from src.domain.entities.user import User

class RegisterUser(UserRepository):
    def __init__(self):
        ...
        
    def create_user(self, user: User) -> User:
        
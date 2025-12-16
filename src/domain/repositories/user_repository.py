from abc import ABC, abstractmethod
from src.domain.entities.user import User

class UserRepository(ABC):
    
    @abstractmethod
    def create_user(self, user: User) -> User:
        ...

    # @abstractmethod
    # def login(self):
    #     ...

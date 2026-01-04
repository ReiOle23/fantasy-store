from abc import ABC, abstractmethod
from src.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def create(self, name: str, password: str) -> User:
        ...
        
    @abstractmethod
    def login(self, name: str, password: str) -> User:
        ...

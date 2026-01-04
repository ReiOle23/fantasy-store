from abc import ABC, abstractmethod
from src.domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    async def create(self, name: str, password: str) -> User:
        ...
        
    @abstractmethod
    async def login(self, name: str, password: str) -> User:
        ...

    @abstractmethod
    async def add_money(self, user_id: str, token: str, amount: int) -> User:
        ...
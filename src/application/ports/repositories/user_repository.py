from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def create(self, name: str, password: str) -> dict:
        ...
        
    @abstractmethod
    def login(self, name: str, password: str) -> dict:
        ...

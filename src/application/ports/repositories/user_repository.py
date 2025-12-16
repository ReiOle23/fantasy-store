from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, item_id: int):
        ...

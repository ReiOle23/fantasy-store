from abc import ABC, abstractmethod
from src.domain.entities.item import Item

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> dict:
        ...

    @abstractmethod
    def get_items(self) -> list[dict]:
        ...
        
    @abstractmethod
    def buy_item(self, id: int, user_id:str, user_token: str) -> Item:
        ...
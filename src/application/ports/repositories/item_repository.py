from abc import ABC, abstractmethod

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> dict:
        ...

    @abstractmethod
    def get_items(self) -> list[dict]:
        ...
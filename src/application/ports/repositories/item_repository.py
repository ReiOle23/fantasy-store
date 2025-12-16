from abc import ABC, abstractmethod

class ItemRepository(ABC):
    @abstractmethod
    def get_by_id(self, item_id: int):
        ...

from src.domain.entities.item import Item
from src.infrastructure.database import Database
from src.application.ports.repositories.item_repository import ItemRepository

class ItemService(ItemRepository):
    def __init__(self):
        self.db = Database
    
    def get_items(self) -> list[dict]:
        return self.db.get_all("Item")

    def get_by_id(self, item_id: int) -> dict:
        return self.db.get_obj("Item", item_id)

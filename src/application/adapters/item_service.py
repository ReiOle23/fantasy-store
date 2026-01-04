from src.infrastructure.database import Database
from src.application.ports.repositories.item_repository import ItemRepository
from src.domain.entities.user import User
from src.domain.entities.item import Item
import asyncio, threading

class ItemService(ItemRepository):
    def __init__(self):
        self.db = Database
        self._lock = threading.Lock()
    
    def get_items(self) -> list[Item]:
        return self.db.get_all(Item)

    def get_by_id(self, item_id: str) -> Item:
        return self.db.get_obj(Item, item_id)

    def buy_item_sync(self, item_id: str, user_id: str, user_token: str) -> Item:
        with self._lock:
            item_obj = self.db.get_obj(Item, item_id)
            if item_obj is None:
                raise ValueError("Item not found")
            if item_obj.owner is not None:
                raise ValueError("Item already owned")

            user_obj = self.db.get_obj(User, user_id)
            if user_obj is None:
                raise ValueError("User not found")
            if user_obj.token != user_token:
                raise ValueError("Invalid user token")
            
            item_obj.owner = user_obj
            self.db.save_obj(item_obj)
            return item_obj

    async def buy_item(self, item_id: str, user_id: str, user_token: str) -> Item:
        return await asyncio.to_thread(self.buy_item_sync, item_id, user_id, user_token)
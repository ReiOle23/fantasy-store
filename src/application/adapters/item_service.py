from src.infrastructure.database import MongoDB
from src.application.ports.repositories.item_repository import ItemRepository
from src.domain.entities.user import User
from src.domain.entities.item import Item
import asyncio, threading, uuid

class ItemService(ItemRepository):
    def __init__(self):
        self.db = MongoDB
    
    async def get_items(self) -> list[Item]:
        return await self.db.get_all(Item)

    async def get_by_id(self, item_id: str) -> Item:
        return await self.db.get_obj(Item, item_id)

    def _duplicate_item(self, item: Item, user_id: str, quantity: int) -> Item:
        new_item = Item(
            id=str(uuid.uuid4()),
            name=item.name,
            owner=user_id,
            quantity=quantity,
            price=item.price
        )
        return new_item
    
    def check_valid_item(self, item_obj: Item):
        if item_obj is None:
            raise Exception("Item not found")
        if item_obj.owner is not None:
            raise Exception("Item already owned")
        if item_obj.quantity <= 0:
            raise Exception("Item out of stock")
        
    def check_valid_user(self, user_obj: User, user_token: str):
        if user_obj is None:
            raise Exception("User not found")
        if user_obj.token != user_token:
            raise Exception("Invalid user token")

    async def process_purchase(self, user_obj: User, item_obj: Item, quantity: int, total_price: int):             
        user_obj.money -= total_price
        user_obj.add_item(self._duplicate_item(item_obj, user_obj.id, quantity))
        # TODO should be atomic because if fails save_obj, then user_obj money is deducted but item not added
        await self.db.save_obj(user_obj)

    async def buy_item(self, item_id: str, user_id: str, user_token: str, quantity: int = 1) -> Item:
        user_obj = await self.db.get_obj(User, user_id)
        self.check_valid_user(user_obj, user_token)

        item_obj = await self.db.get_obj(Item, item_id)
        self.check_valid_item(item_obj)
        
        total_price = item_obj.price * quantity
        if total_price > user_obj.money:
            raise Exception("Not enough money to buy the item(s)")
                
        result = await self.db.update_one(
            Item,
            {"_id": item_id, "quantity": {"$gte": quantity}},
            {"$inc": {"quantity": -quantity}}
        )
        if result.modified_count == 0:
            raise Exception("Item sold out or insufficient quantity")
        
        await self.process_purchase(user_obj, item_obj, quantity, total_price)
        
        # Check if we need to delete the item
        updated_item = await self.db.get_obj(Item, item_id)
        if updated_item.quantity <= 0:
            await self.db.remove_obj(updated_item)
        
        return item_obj
        
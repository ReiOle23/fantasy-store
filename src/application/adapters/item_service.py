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
            raise ValueError("Item not found")
        if item_obj.owner is not None:
            raise ValueError("Item already owned")
        
    def check_valid_user(self, user_obj: User, user_token: str):
        if user_obj is None:
            raise ValueError("User not found")
        if user_obj.token != user_token:
            raise ValueError("Invalid user token")

    async def update_user_money(self, user_obj: User, item_obj: Item, quantity: int):
        total_price = item_obj.price * quantity
        if total_price > user_obj.money:
            raise Exception("Not enough money to buy the item(s)")
                    
        user_obj.money -= total_price
        user_obj.add_item(self._duplicate_item(item_obj, user_obj.id, quantity))
        await self.db.save_obj(user_obj)

    async def buy_item(self, item_id: str, user_id: str, user_token: str, quantity: int = 1) -> Item:
        client = self.db.client
        async with await client.start_session() as s:
            async with s.start_transaction():
                user_obj = await self.db.get_obj(User, user_id)
                self.check_valid_user(user_obj, user_token)
        
                item_obj = await self.db.get_obj(Item, item_id)
                self.check_valid_item(item_obj)
                
                await self.update_user_money(user_obj, item_obj, quantity)
                item_obj.quantity -= quantity
                if item_obj.quantity <= 0:
                    await self.db.remove_obj(item_obj)
                else:
                    await self.db.save_obj(item_obj)
                
        return item_obj
        
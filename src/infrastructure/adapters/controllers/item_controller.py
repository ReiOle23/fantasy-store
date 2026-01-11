from src.infrastructure.adapters.schemas.item import ItemObject, UserItemRequest
from src.application.adapters.item_service import ItemService

class ItemController:
    def __init__(self):
        self.use_case = ItemService()
        
    async def get_items(self) -> list[ItemObject]:
        items = await self.use_case.get_items()
        return [ItemObject(
            id=item.id,
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            owner=item.owner
        ) for item in items]

    async def get_item_by_id(self, item_id: str) -> ItemObject:
        item = await self.use_case.get_by_id(item_id)
        return ItemObject(
            id=item.id,
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            owner=item.owner
        )

    async def buy_item(self, payload: UserItemRequest) -> ItemObject:
        item = await self.use_case.buy_item(payload.item_id, payload.user_id, payload.user_token, payload.quantity)
        return ItemObject(
            id=item.id, 
            name=item.name, 
            quantity=item.quantity,
            price=item.price,
            owner=item.owner
            )
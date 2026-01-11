from fastapi import APIRouter, status
from src.infrastructure.adapters.schemas.item import ItemObject, UserItemRequest
from src.infrastructure.adapters.controllers.item_controller import ItemController

router = APIRouter()

@router.get("/items", tags=["items"], response_model=list[ItemObject], status_code=status.HTTP_201_CREATED)
async def get_items() -> list[ItemObject]:
	return await ItemController().get_items()

@router.get("/items/{item_id}", tags=["items"], response_model=ItemObject, status_code=status.HTTP_201_CREATED)
async def get_item(item_id: str) -> ItemObject:
	return await ItemController().get_item_by_id(item_id)

@router.post("/buy-item", tags=["items"], response_model=ItemObject, status_code=status.HTTP_201_CREATED)
async def buy_item(payload: UserItemRequest) -> ItemObject:
	return await ItemController().buy_item(payload)
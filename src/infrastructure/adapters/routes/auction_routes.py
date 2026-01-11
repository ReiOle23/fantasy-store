from fastapi import APIRouter, HTTPException, status
from src.domain.entities import item
from src.infrastructure.adapters.schemas.item import ItemObject, UserItemRequest
from src.infrastructure.adapters.controllers.item_controller import ItemController

router = APIRouter()

@router.get("/items", tags=["items"], response_model=list[ItemObject], status_code=status.HTTP_201_CREATED)
async def get_items() -> list[ItemObject]:
	return await ItemController().get_items()

@router.get("/items/{item_id}", tags=["items"], response_model=ItemObject, status_code=status.HTTP_200_OK)
async def get_item(item_id: str) -> ItemObject:
	item = await ItemController().get_item_by_id(item_id)
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")    
	return item

@router.post("/buy-item", tags=["items"], response_model=ItemObject, status_code=status.HTTP_200_OK)
async def buy_item(payload: UserItemRequest) -> ItemObject:
	item = await ItemController().buy_item(payload)
	if not item:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found") 
	return item
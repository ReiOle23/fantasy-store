from pydantic import BaseModel, Field
from typing import List

class UserItemRequest(BaseModel):
    item_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    user_token: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)


class ItemObject(BaseModel):
    id: str
    name: str
    quantity: int
    price: int
    owner: str | None = None
    
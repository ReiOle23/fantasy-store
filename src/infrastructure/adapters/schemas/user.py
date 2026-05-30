from pydantic import BaseModel, Field
from typing import List
from src.infrastructure.adapters.schemas.item import ItemObject

class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    
class UserTokenRequest(BaseModel):
    id: str = Field(..., min_length=1)
    token: str = Field(..., min_length=1)
    amount: int = Field(..., gt=0)

class UserSetNameRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    user_token: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)

class UserSetMoneyRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    user_token: str = Field(..., min_length=1)
    amount: int = Field(..., ge=0)

class UserAddItemRequest(BaseModel):
    user_id: str = Field(..., min_length=1)
    user_token: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    price: int = Field(..., ge=0)
    quantity: int = Field(1, gt=0)
    item_type: str = Field(..., min_length=1)
    properties: dict = {}

class UserResponse(BaseModel):
    id: str
    name: str
    token: str
    items: List[ItemObject] = Field(default_factory=list)
    money: int

class UserObject(BaseModel):
    id: str
    name: str
    token: str
    
class UserPublicObject(BaseModel):
    id: str
    name: str
    
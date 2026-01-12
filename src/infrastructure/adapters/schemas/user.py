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
    
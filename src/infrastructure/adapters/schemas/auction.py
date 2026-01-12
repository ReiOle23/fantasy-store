from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from src.infrastructure.adapters.schemas.item import ItemObject
from src.infrastructure.adapters.schemas.user import UserPublicObject

class AuctionBidRequest(BaseModel):
    auction_id: str = Field(..., min_length=1)
    user_id: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    
    
class AuctionCreateRequest(BaseModel):
    item_id: str
    user_id: str
    end_date: datetime
    
class BidObject(BaseModel):
    id: str
    user: UserPublicObject
    price: int
    created_at: datetime
    updated_at: datetime
    

class AuctionObject(BaseModel):
    id: str
    item: ItemObject
    user: UserPublicObject
    start_date: datetime
    end_date: datetime
    highest_bid: int = 0
    bids: List[BidObject] = Field(default_factory=list)
    highest_bidder: str | None = None
    
class AuctionPublicObject(BaseModel):
    id: str
    item: ItemObject
    user: UserPublicObject
    start_date: datetime
    end_date: datetime
    highest_bid: int = 0
    highest_bidder: str | None = None
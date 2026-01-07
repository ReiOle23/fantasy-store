from abc import ABC, abstractmethod
from src.domain.entities.auction import Auction
from src.domain.entities.item import Item
from datetime import datetime

class AuctionRepository(ABC):
    @abstractmethod
    async def create_auction(self, item: Item, start_date: datetime, end_date: datetime) -> Auction:
        ...
        
    @abstractmethod
    async def make_bid(self, auction_id:str, user_id: str, price: float) -> bool:
        ...
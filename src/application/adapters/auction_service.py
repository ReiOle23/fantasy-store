from src.application.ports.repositories.auction_repository import AuctionRepository
from src.domain.entities.auction import Auction
from src.domain.entities.item import Item
from datetime import datetime
from src.infrastructure.database import MongoDB
import uuid

class AuctionService(AuctionRepository):
    def __init__(self):
        self.db = MongoDB
    
    async def create_auction(self, item: Item, end_date: datetime) -> Auction:
        new_auction = Auction(
            id=str(uuid.uuid4()),
            item=item,
            start_date=datetime.now(),
            end_date=end_date,
        )
        await self.db.save_obj(new_auction)
        return new_auction
        
    async def make_bid(self, auction_id:str, user_id: str, price: float) -> bool:
        ...
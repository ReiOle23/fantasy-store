from dataclasses import asdict
from src.application.ports.repositories.auction_repository import AuctionRepository
from src.domain.entities.auction import Auction
from src.domain.entities.user import User
from src.domain.entities.item import Item
from src.domain.entities.bid import Bid
from datetime import datetime
from src.infrastructure.database import MongoDB
import uuid, asyncio

class AuctionService(AuctionRepository):
    def __init__(self):
        self.db = MongoDB
    
    async def create_auction(self, item: Item, user: User, end_date: datetime) -> Auction:
        new_auction = Auction(
            id=str(uuid.uuid4()),
            item=item,
            user=user,
            start_date=datetime.now(),
            end_date=end_date,
            highest_bid=item.price
        )
        await self.db.save_obj(new_auction)
        return new_auction
    
    async def _checks_before_bid(self, auction: Auction, user: User, price: float):
        if auction is None:
            raise Exception("Auction not found")
        if user is None:
            raise Exception("User not found")
        
        if user.money < price:
            raise Exception("User does not have enough money to make this bid")
        
        if datetime.now() > auction.end_date:
            raise Exception("Auction has expired")
        
        if price <= auction.highest_bid:
            raise Exception("Bid price must be higher than the current highest bid")
        
    async def make_bid(self, auction_id:str, user_id: str, price: float) -> bool:
        auction, user = await asyncio.gather(
            self.db.get_obj(Auction, auction_id),
            self.db.get_obj(User, user_id)
        )
        await self._checks_before_bid(auction, user, price)
        
        old_highest_bid = auction.highest_bid
        new_bid = Bid(
            user=user_id,
            price=price
        )
        auction.bids.append(new_bid)
        auction.highest_bid = price
        auction.highest_bidder = user_id
        
        result = await self.db.update_one(
            Auction,
            {
                "_id": auction_id,
                "highest_bid": old_highest_bid,
                "end_date": {"$gt": datetime.now()},
            },
            {
                "$push": {"bids": asdict(new_bid)},
                "$set": {"highest_bid": price, "highest_bidder": user_id}
            }
        )

        if result.modified_count == 0:
            raise Exception("Auction state changed, please retry")
        
        return True
    
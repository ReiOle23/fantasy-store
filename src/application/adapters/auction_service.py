from dataclasses import asdict
from src.application.ports.repositories.auction_repository import AuctionRepository
from src.domain.entities.auction import Auction
from src.domain.entities.user import User
from src.domain.entities.bid import Bid
from datetime import datetime
from src.infrastructure.database import MongoDB
import uuid, asyncio
from fastapi import HTTPException, status

class AuctionService(AuctionRepository):
    def __init__(self):
        self.db = MongoDB
        
    async def get_auctions(self) -> list[Auction]:
        return await self.db.get_all(Auction)
    
    async def _user_winner_process(self, auction: Auction):
        user_winner = await self.db.get_obj(User, auction.highest_bidder)
        user_winner.money -= auction.highest_bid
        user_winner.add_item(auction.item)
        await self.db.save_obj(user_winner)
        
    async def _auction_user_save_money(self, auction: Auction):
        auction_user = await self.db.get_obj(User, auction.user.id)
        auction_user.money += auction.highest_bid
        await self.db.save_obj(auction_user)
    
    async def _finish_auction(self, auction: Auction):
        if auction.highest_bidder is not None:
            await self._user_winner_process(auction)
            await self._auction_user_save_money(auction)
        else:
            auction.user.add_item(auction.item)
            await self.db.save_obj(auction.user)
            
    async def _auction_user_remove_item(self, auction: Auction):
        auction.user.remove_item(auction.item)
        await self.db.save_obj(auction.user)
            
    async def get_auction(self, auction_id: str) -> Auction:
        auction = await self.db.get_obj(Auction, auction_id)
        if auction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction not found")
        if datetime.now() > auction.end_date:
            self._finish_auction(auction)
        return auction

    async def create_auction(self, item_id: str, user_id: str, end_date: datetime) -> Auction:
        user = await self.db.get_obj(User, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        item = user.get_item(item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
       
        new_auction = Auction(
            id=str(uuid.uuid4()),
            item=item,
            user=user,
            start_date=datetime.now(),
            end_date=end_date,
            highest_bid=item.price
        )
        await self.db.save_obj(new_auction)
        await self._auction_user_remove_item(new_auction)
        return new_auction
    
    async def _checks_before_bid(self, auction: Auction, user: User, price: float):
        if auction is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction not found")
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        if user.money < price:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not have enough money to make this bid")
        
        if datetime.now() > auction.end_date:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction has expired")

        if price <= auction.highest_bid:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bid price must be higher than the current highest bid")
        
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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction state changed, please retry")
        
        return True
    
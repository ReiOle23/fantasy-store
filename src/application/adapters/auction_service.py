from dataclasses import asdict
from src.application.ports.repositories.auction_repository import AuctionRepository
from src.domain.entities import auction
from src.domain.entities.auction import Auction
from src.domain.entities.user import User
from src.domain.entities.bid import Bid
from datetime import datetime
from src.infrastructure.database import MongoDB
import uuid, asyncio, logging
from fastapi import HTTPException, status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuctionService(AuctionRepository):
    def __init__(self):
        self.db = MongoDB
        
    async def get_auctions(self) -> list[Auction]:
        return await self.db.get_all(Auction)
    
    async def _give_item(self, user_id: str, auction: Auction, money_change: int = 0):
        """Atomically push the auctioned item into a user's inventory (and move gold), without
        overwriting the rest of the user document."""
        auction.item.owner = user_id
        update = {"$push": {"items": asdict(auction.item)}}
        if money_change:
            update["$inc"] = {"money": money_change}
        await self.db.update_one(User, {"_id": user_id}, update)

    async def _user_winner_process(self, auction: Auction):
        await self._give_item(auction.highest_bidder, auction, -auction.highest_bid)

    async def _auction_user_save_money(self, auction: Auction):
        await self.db.update_one(User, {"_id": auction.user.id}, {"$inc": {"money": auction.highest_bid}})

    async def finish_auction(self, auction: Auction):
        if auction.rewarded:
            return
        # Claim the delivery atomically so concurrent finishes deliver exactly once.
        claim = await self.db.update_one(
            Auction,
            {"_id": auction.id, "rewarded": False},
            {"$set": {"rewarded": True}},
        )
        auction.rewarded = True
        if claim.modified_count != 1:
            return
        logger.info(f"✓ Auction with id {auction.id} ended")
        if auction.highest_bidder != None:
            await self._user_winner_process(auction)
            await self._auction_user_save_money(auction)
        else:
            await self._give_item(auction.user.id, auction)

    async def _auction_user_remove_item(self, user_id: str, item_id: str) -> bool:
        """Atomically take the item out of the seller's inventory. False if it was no longer there."""
        result = await self.db.update_one(
            User,
            {"_id": user_id, "items.id": item_id},
            {"$pull": {"items": {"id": item_id}}},
        )
        return result.modified_count == 1

    async def get_auction(self, auction_id: str) -> Auction:
        auction_obj = await self.db.get_obj(Auction, auction_id)
        if auction_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction not found")
        if datetime.now() > auction_obj.end_date:
            await self.finish_auction(auction_obj)
        return auction_obj

    async def settle_pending(self) -> list[Auction]:
        """Finish ended auctions and atomically claim the in-game settlement slot. Returns the newly-settled ones."""
        now = datetime.now()
        newly_settled: list[Auction] = []
        for auct in await self.db.get_all(Auction):
            if auct.settled_in_game or now < auct.end_date:
                continue
            if not auct.rewarded:
                await self.finish_auction(auct)
            result = await self.db.update_one(
                Auction,
                {"_id": auct.id, "settled_in_game": False},
                {"$set": {"settled_in_game": True}},
            )
            if result.modified_count == 1:
                refreshed = await self.db.get_obj(Auction, auct.id)
                if refreshed is not None:
                    newly_settled.append(refreshed)
        return newly_settled

    async def pending_settlements(self) -> list[Auction]:
        """Finish every ended auction (idempotent) and return those not yet pushed to the game."""
        now = datetime.now()
        pending: list[Auction] = []
        for auct in await self.db.get_all(Auction):
            if auct.settled_in_game or now < auct.end_date:
                continue
            if not auct.rewarded:
                await self.finish_auction(auct)
            pending.append(auct)
        return pending

    async def claim_settled(self, auction_id: str) -> bool:
        """Atomically mark an auction as pushed to the game. Returns True only for the claiming caller."""
        result = await self.db.update_one(
            Auction,
            {"_id": auction_id, "settled_in_game": False},
            {"$set": {"settled_in_game": True}},
        )
        return result.modified_count == 1

    async def mark_settled_in_game(self, auction_id: str) -> Auction:
        auction_obj = await self.db.get_obj(Auction, auction_id)
        if auction_obj is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction not found")
        if datetime.now() < auction_obj.end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Auction not ended yet")
        if not auction_obj.rewarded:
            await self.finish_auction(auction_obj)

        result = await self.db.update_one(
            Auction,
            {"_id": auction_id, "settled_in_game": False},
            {"$set": {"settled_in_game": True}},
        )
        if result.modified_count != 1:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Auction already settled in game")
        return await self.db.get_obj(Auction, auction_id)

    async def create_auction(self, item_id: str, user_id: str, end_date: datetime, starting_bid: int = None) -> Auction:
        user = await self.db.get_obj(User, user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        item = user.get_item(item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        if not item.is_auctionable():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item cannot be auctioned")

        # The item leaves the inventory first, atomically, so it can only be in one auction.
        if not await self._auction_user_remove_item(user_id, item_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        user.remove_item(item_id)

        new_auction = Auction(
            id=str(uuid.uuid4()),
            item=item,
            user=user,
            start_date=datetime.now(),
            end_date=end_date,
            highest_bid=starting_bid if starting_bid is not None else item.price
        )
        await self.db.save_obj(new_auction)
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
    
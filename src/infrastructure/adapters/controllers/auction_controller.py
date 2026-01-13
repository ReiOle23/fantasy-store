from src.infrastructure.adapters.schemas.auction import AuctionBidRequest, AuctionCreateRequest
from src.infrastructure.adapters.schemas.auction import AuctionObject, AuctionPublicObject, BidObject
from src.infrastructure.adapters.schemas.item import ItemObject
from src.infrastructure.adapters.schemas.user import UserPublicObject
from src.application.adapters.auction_service import AuctionService
from src.infrastructure.database import MongoDB
from src.domain.entities.user import User

class AuctionController:
    def __init__(self):
        self.use_case = AuctionService()
        self.db = MongoDB()
        
    def _public_user_obj(self, user):
        if not user:
            return None
        return UserPublicObject(
            id=user.id,
            name=user.name
        )
        
    async def get_bids_obj(self, bids: list[BidObject]):
        user_ids = list({bid.user for bid in bids})
        users = await self.db.get_objs(User, user_ids)
        user_map = {user.id: user for user in users}

        return [
            BidObject(
                id=bid.id,
                user=self._public_user_obj(user_map[bid.user]),
                price=bid.price,
                created_at=bid.created_at,
                updated_at=bid.updated_at
            )
            for bid in bids
        ]
    
    async def _return_auction_object(self, auction) -> AuctionObject:
        highest_bidder = await self.db.get_obj(User, auction.highest_bidder) if auction.highest_bidder else None
        bids_objects = await self.get_bids_obj(auction.bids)
        return AuctionObject(
            id=auction.id,
            item=ItemObject(
                    id=auction.item.id,
                    name=auction.item.name,
                    quantity=auction.item.quantity,
                    price=auction.item.price,
                    owner=auction.item.owner
                ),
            user=self._public_user_obj(auction.user),
            start_date=auction.start_date,
            end_date=auction.end_date,
            highest_bid=auction.highest_bid,
            bids=bids_objects,
            highest_bidder=self._public_user_obj(highest_bidder),
            rewarded=auction.rewarded
        )

    async def _return_public_auction_object(self, auction) -> AuctionPublicObject:
        highest_bidder = await self.db.get_obj(User, auction.highest_bidder) if auction.highest_bidder else None
        return AuctionPublicObject(
            id=auction.id,
            item=ItemObject(
                    id=auction.item.id,
                    name=auction.item.name,
                    quantity=auction.item.quantity,
                    price=auction.item.price,
                    owner=auction.item.owner
                ),
            user=self._public_user_obj(auction.user),
            start_date=auction.start_date,
            end_date=auction.end_date,
            highest_bid=auction.highest_bid,
            highest_bidder=self._public_user_obj(highest_bidder),
            rewarded=auction.rewarded
        )

    async def get_auctions(self) -> list[AuctionPublicObject]:
        auctions = await self.use_case.get_auctions()
        return [await self._return_public_auction_object(auction) for auction in auctions]
    
    async def get_auction(self, auction_id: str) -> AuctionObject:
        auction = await self.use_case.get_auction(auction_id)
        return await self._return_auction_object(auction)
    
    async def create_auction(self, payload: AuctionCreateRequest) -> AuctionPublicObject:
        auction = await self.use_case.create_auction(payload.item_id, payload.user_id, payload.end_date)
        return await self._return_public_auction_object(auction)

    async def make_bid(self, payload: AuctionBidRequest) -> bool:
        return await self.use_case.make_bid(payload.auction_id, payload.user_id, payload.price)

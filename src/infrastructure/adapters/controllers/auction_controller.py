from src.infrastructure.adapters.schemas.auction import AuctionBidRequest, AuctionCreateRequest
from src.infrastructure.adapters.schemas.auction import AuctionObject, AuctionPublicObject, BidObject
from src.infrastructure.adapters.schemas.item import ItemObject
from src.infrastructure.adapters.schemas.user import UserPublicObject
from src.application.adapters.auction_service import AuctionService

class AuctionController:
    def __init__(self):
        self.use_case = AuctionService()
    
    def _return_auction_object(self, auction) -> AuctionObject:
        return AuctionObject(
            id=auction.id,
            item=ItemObject(
                    id=auction.item.id,
                    name=auction.item.name,
                    quantity=auction.item.quantity,
                    price=auction.item.price,
                    owner=auction.item.owner
                ),
            user=UserPublicObject(
                    id=auction.user.id,
                    name=auction.user.name
                ),
            start_date=auction.start_date,
            end_date=auction.end_date,
            highest_bid=auction.highest_bid,
            bids=[
                BidObject(
                    id=bid.id,
                    user=UserPublicObject(
                        id=bid.user.id,
                        name=bid.user.name
                    ),
                    price=bid.price,
                    created_at=bid.created_at,
                    updated_at=bid.updated_at
                )
                for bid in auction.bids
            ],
            highest_bidder=auction.highest_bidder
        )

    def _return_public_auction_object(self, auction) -> AuctionPublicObject:
        return AuctionPublicObject(
            id=auction.id,
            item=ItemObject(
                    id=auction.item.id,
                    name=auction.item.name,
                    quantity=auction.item.quantity,
                    price=auction.item.price,
                    owner=auction.item.owner
                ),
            user=UserPublicObject(
                    id=auction.user.id,
                    name=auction.user.name
                ),
            start_date=auction.start_date,
            end_date=auction.end_date,
            highest_bid=auction.highest_bid,
            highest_bidder=auction.highest_bidder
        )

    async def get_auctions(self) -> list[AuctionPublicObject]:
        auctions = await self.use_case.get_auctions()
        return [self._return_public_auction_object(auction) for auction in auctions]
    
    async def get_auction(self, auction_id: str) -> AuctionObject:
        auction = await self.use_case.get_auction(auction_id)
        return self._return_auction_object(auction)

    async def create_auction(self, payload: AuctionCreateRequest) -> AuctionPublicObject:
        auction = await self.use_case.create_auction(payload.item_id, payload.user_id, payload.end_date)
        return self._return_public_auction_object(auction)

    async def make_bid(self, payload: AuctionBidRequest) -> bool:
        return await self.use_case.make_bid(payload.auction_id, payload.user_id, payload.price)
             
from fastapi import APIRouter, HTTPException, status
from src.infrastructure.adapters.schemas.auction import AuctionCreateRequest, AuctionBidRequest
from src.infrastructure.adapters.schemas.auction import AuctionObject, AuctionPublicObject
from src.infrastructure.adapters.controllers.auction_controller import AuctionController

router = APIRouter()

@router.get("/auctions", tags=["auctions"], response_model=list[AuctionPublicObject], status_code=status.HTTP_201_CREATED)
async def get_auctions() -> list[AuctionPublicObject]:
	return await AuctionController().get_auctions()

@router.get("/auction/{auction_id}", tags=["auctions"], response_model=AuctionObject, status_code=status.HTTP_200_OK)
async def get_auction(auction_id: str) -> AuctionObject:
	return await AuctionController().get_auction(auction_id)

@router.post("/auctions", tags=["auctions"], response_model=AuctionPublicObject, status_code=status.HTTP_201_CREATED)
async def create_auction(payload: AuctionCreateRequest) -> AuctionPublicObject:
	return await AuctionController().create_auction(payload)

@router.post("/auctions/{auction_id}/bid", tags=["auctions"], response_model=bool, status_code=status.HTTP_200_OK)
async def make_bid(payload: AuctionBidRequest) -> bool:
	return await AuctionController().make_bid(payload)
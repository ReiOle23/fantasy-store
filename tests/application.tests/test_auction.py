import asyncio, pytest
from src.infrastructure.database import MongoDB
from src.domain.entities.auction import Auction
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_auction(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    auction = await auction_service.create_auction(user.items[0], datetime.now() + timedelta(minutes=1))
    assert await MongoDB.get_obj(Auction, auction.id) is not None
    assert auction.item.name == f"{user.name}'s Staff"
    
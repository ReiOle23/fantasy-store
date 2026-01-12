import asyncio, pytest
from src.infrastructure.database import MongoDB
from src.domain.entities.auction import Auction
from src.domain.entities.user import User
from datetime import datetime, timedelta

@pytest.mark.asyncio
async def test_create_auction(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(minutes=1)
    )
    assert await MongoDB.get_obj(Auction, auction.id) is not None
    assert auction.item.name == f"{user.name}'s Staff"
    
@pytest.mark.asyncio
async def test_auction_user_make_bid_for_less_error(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    user2 = await auction_init_user("user2")
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(minutes=1)
    )
    with pytest.raises(Exception):
        await auction_service.make_bid(auction.id, user2.id, 25)
        
@pytest.mark.asyncio
async def test_auction_user_make_bid_has_no_money(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    user2 = await auction_init_user("user2")
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(minutes=1)
    )
    with pytest.raises(Exception):
        await auction_service.make_bid(auction.id, user2.id, 1100)
        
@pytest.mark.asyncio
async def test_bid_on_expired_auction_raises_error(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    user2 = await auction_init_user("user2")
    # Create auction that expires immediately
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(milliseconds=1)
    )
    
    await asyncio.sleep(0.01)
    with pytest.raises(Exception):
        await auction_service.make_bid(auction.id, user2.id, 100)
        
@pytest.mark.asyncio
async def test_bid_after_another_bid(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    user2 = await auction_init_user("user2")
    user3 = await auction_init_user("user3")
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(minutes=5)
    )
    
    await auction_service.make_bid(auction.id, user2.id, 100)
    await auction_service.make_bid(auction.id, user3.id, 150)
    updated_auction = await MongoDB.get_obj(Auction, auction.id)
    assert updated_auction.highest_bid == 150

@pytest.mark.repeat(5)
@pytest.mark.asyncio
async def test_three_bids_same_time(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    user2 = await auction_init_user("user2")
    user3 = await auction_init_user("user3")
    user4 = await auction_init_user("user4")
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(minutes=1)
    )
    
    tasks = [asyncio.create_task(auction_service.make_bid(auction.id, user2.id, 100)),
             asyncio.create_task(auction_service.make_bid(auction.id, user3.id, 100)),
             asyncio.create_task(auction_service.make_bid(auction.id, user4.id, 100))
             ]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    assert len(successes) == 1
    
@pytest.mark.asyncio
async def test_auction_ends_without_bids(auction_service, auction_init_user):
    user = await auction_init_user("user1")
    auction = await auction_service.create_auction(
        user.items[0].id or None,
        user.id,
        datetime.now() + timedelta(seconds=1)
    )
    user = await MongoDB.get_obj(User, user.id)
    assert len(user.items) == 0
    await asyncio.sleep(2)
    user_then = await MongoDB.get_obj(User, user.id)
    assert len(user_then.items) == 1
    assert user_then.money == user.money
    
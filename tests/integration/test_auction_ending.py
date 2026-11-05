"""Business rule 15 — when the auction ends: winner gets the item, seller gets the gold
(or the item back), and each auction is delivered exactly once."""
import asyncio
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.infrastructure.database import MongoDB
from src.domain.entities.auction import Auction
from src.domain.entities.user import User


async def open_auction(auction_service, seller):
    return await auction_service.create_auction(
        seller.items[0].id, seller.id, datetime.now() + timedelta(hours=1))


def count_item(user: User, item_id: str) -> int:
    return sum(1 for item in user.items if item.id == item_id)


@pytest.mark.asyncio
async def test_running_auction_is_not_finished_when_read(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)

    fetched = await auction_service.get_auction(auction.id)

    assert fetched.rewarded is False
    assert (await MongoDB.get_obj(User, seller.id)).get_item(auction.item.id) is None


@pytest.mark.asyncio
async def test_winner_gets_item_and_seller_gets_winning_bid(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    loser = await auction_init_user("loser")
    winner = await auction_init_user("winner")
    auction = await open_auction(auction_service, seller)
    await auction_service.make_bid(auction.id, loser.id, 100)
    await auction_service.make_bid(auction.id, winner.id, 300)
    await expire_auction(auction.id)

    await auction_service.get_auction(auction.id)

    stored_winner = await MongoDB.get_obj(User, winner.id)
    stored_loser = await MongoDB.get_obj(User, loser.id)
    stored_seller = await MongoDB.get_obj(User, seller.id)
    assert count_item(stored_winner, auction.item.id) == 1
    assert stored_winner.get_item(auction.item.id).owner == winner.id
    assert stored_winner.money == winner.money - 300
    assert stored_seller.money == seller.money + 300
    assert stored_seller.get_item(auction.item.id) is None
    assert stored_loser.get_item(auction.item.id) is None
    assert stored_loser.money == loser.money


@pytest.mark.asyncio
async def test_item_returns_to_seller_when_nobody_bid(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    await auction_service.get_auction(auction.id)

    stored_seller = await MongoDB.get_obj(User, seller.id)
    assert count_item(stored_seller, auction.item.id) == 1
    assert stored_seller.money == seller.money


@pytest.mark.asyncio
async def test_ended_auction_is_delivered_once_when_read_many_times(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    winner = await auction_init_user("winner")
    auction = await open_auction(auction_service, seller)
    await auction_service.make_bid(auction.id, winner.id, 200)
    await expire_auction(auction.id)

    for _ in range(3):
        await auction_service.get_auction(auction.id)

    stored_winner = await MongoDB.get_obj(User, winner.id)
    stored_seller = await MongoDB.get_obj(User, seller.id)
    assert count_item(stored_winner, auction.item.id) == 1
    assert stored_winner.money == winner.money - 200
    assert stored_seller.money == seller.money + 200
    assert (await MongoDB.get_obj(Auction, auction.id)).rewarded is True


@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_ended_auction_read_at_the_same_moment_is_delivered_once(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    winner = await auction_init_user("winner")
    auction = await open_auction(auction_service, seller)
    await auction_service.make_bid(auction.id, winner.id, 200)
    await expire_auction(auction.id)

    await asyncio.gather(*(auction_service.get_auction(auction.id) for _ in range(10)))

    stored_winner = await MongoDB.get_obj(User, winner.id)
    stored_seller = await MongoDB.get_obj(User, seller.id)
    assert count_item(stored_winner, auction.item.id) == 1
    assert stored_winner.money == winner.money - 200
    assert stored_seller.money == seller.money + 200


@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_unsold_auction_read_at_the_same_moment_returns_item_once(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    await asyncio.gather(*(auction_service.get_auction(auction.id) for _ in range(10)))

    stored_seller = await MongoDB.get_obj(User, seller.id)
    assert count_item(stored_seller, auction.item.id) == 1


@pytest.mark.asyncio
async def test_unknown_auction_is_not_found(auction_service):
    with pytest.raises(HTTPException) as error:
        await auction_service.get_auction("no-such-auction")
    assert error.value.status_code == 404

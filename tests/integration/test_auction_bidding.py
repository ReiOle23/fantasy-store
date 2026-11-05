"""Business rule 15 — bidding, and many bids at the same moment."""
import asyncio
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.infrastructure.database import MongoDB
from src.domain.entities.auction import Auction


async def open_auction(auction_service, seller, starting_bid=None):
    return await auction_service.create_auction(
        seller.items[0].id, seller.id, datetime.now() + timedelta(hours=1), starting_bid)


@pytest.mark.asyncio
async def test_bid_equal_to_current_bid_is_rejected(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidder = await auction_init_user("bidder")
    auction = await open_auction(auction_service, seller, starting_bid=100)

    with pytest.raises(HTTPException) as error:
        await auction_service.make_bid(auction.id, bidder.id, 100)
    assert "higher" in error.value.detail


@pytest.mark.asyncio
async def test_bid_must_beat_the_last_bid_not_only_the_start_price(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    first = await auction_init_user("first")
    second = await auction_init_user("second")
    auction = await open_auction(auction_service, seller)
    await auction_service.make_bid(auction.id, first.id, 200)

    with pytest.raises(HTTPException):
        await auction_service.make_bid(auction.id, second.id, 150)

    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.highest_bid == 200
    assert stored.highest_bidder == first.id


@pytest.mark.asyncio
async def test_bid_of_all_the_bidders_gold_is_accepted(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidder = await auction_init_user("bidder")  # has 1000 gold
    auction = await open_auction(auction_service, seller)

    assert await auction_service.make_bid(auction.id, bidder.id, 1000) is True


@pytest.mark.asyncio
async def test_unaffordable_bid_leaves_auction_unchanged(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidder = await auction_init_user("bidder")
    auction = await open_auction(auction_service, seller)

    with pytest.raises(HTTPException) as error:
        await auction_service.make_bid(auction.id, bidder.id, 1001)
    assert "money" in error.value.detail

    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.bids == []
    assert stored.highest_bidder is None


@pytest.mark.asyncio
async def test_bid_after_the_end_is_rejected(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    bidder = await auction_init_user("bidder")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    with pytest.raises(HTTPException) as error:
        await auction_service.make_bid(auction.id, bidder.id, 500)
    assert "expired" in error.value.detail
    assert (await MongoDB.get_obj(Auction, auction.id)).highest_bidder is None


@pytest.mark.asyncio
async def test_bid_on_unknown_auction_is_rejected(auction_service, auction_init_user):
    bidder = await auction_init_user("bidder")

    with pytest.raises(HTTPException) as error:
        await auction_service.make_bid("no-such-auction", bidder.id, 500)
    assert error.value.status_code == 404


@pytest.mark.asyncio
async def test_accepted_bid_is_recorded_and_bidder_leads(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidder = await auction_init_user("bidder")
    auction = await open_auction(auction_service, seller)

    await auction_service.make_bid(auction.id, bidder.id, 120)

    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.highest_bid == 120
    assert stored.highest_bidder == bidder.id
    assert [(b.user, b.price) for b in stored.bids] == [(bidder.id, 120)]


@pytest.mark.asyncio
async def test_bidder_can_raise_their_own_bid(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidder = await auction_init_user("bidder")
    auction = await open_auction(auction_service, seller)

    await auction_service.make_bid(auction.id, bidder.id, 100)
    await auction_service.make_bid(auction.id, bidder.id, 150)

    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.highest_bid == 150
    assert stored.highest_bidder == bidder.id


@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_simultaneous_bids_at_different_prices_never_lower_the_price(auction_service, auction_init_user):
    """A bid read after another was stored is a later bid and may win against it; but the
    accepted bids must form a strictly rising chain and the auction must end on the last one."""
    seller = await auction_init_user("seller")
    bidders = [await auction_init_user(f"user{i}") for i in range(10)]
    auction = await open_auction(auction_service, seller)
    prices = [100 + 10 * i for i in range(10)]

    results = await asyncio.gather(
        *(auction_service.make_bid(auction.id, b.id, p) for b, p in zip(bidders, prices)),
        return_exceptions=True,
    )

    accepted = {b.id: p for b, p, r in zip(bidders, prices, results) if not isinstance(r, Exception)}
    assert len(accepted) >= 1
    stored = await MongoDB.get_obj(Auction, auction.id)
    stored_prices = [bid.price for bid in stored.bids]
    assert {bid.user: bid.price for bid in stored.bids} == accepted
    assert stored_prices == sorted(set(stored_prices))
    assert stored.highest_bid == stored_prices[-1]
    assert stored.highest_bidder == stored.bids[-1].user


@pytest.mark.repeat(5)
@pytest.mark.asyncio
async def test_rejected_simultaneous_bidders_are_told_the_price_changed(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidders = [await auction_init_user(f"user{i}") for i in range(5)]
    auction = await open_auction(auction_service, seller)

    results = await asyncio.gather(
        *(auction_service.make_bid(auction.id, b.id, 100) for b in bidders),
        return_exceptions=True,
    )

    rejected = [r for r in results if isinstance(r, Exception)]
    assert len(rejected) == 4
    for error in rejected:
        assert isinstance(error, HTTPException)
        assert "changed" in error.detail or "higher" in error.detail


@pytest.mark.asyncio
async def test_rejected_bidder_can_bid_again_above_the_new_price(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    bidders = [await auction_init_user(f"user{i}") for i in range(3)]
    auction = await open_auction(auction_service, seller)

    results = await asyncio.gather(
        *(auction_service.make_bid(auction.id, b.id, 100) for b in bidders),
        return_exceptions=True,
    )
    loser = next(b for b, r in zip(bidders, results) if isinstance(r, Exception))

    assert await auction_service.make_bid(auction.id, loser.id, 110) is True
    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.highest_bidder == loser.id

"""Business rule 15 — each finished auction produces the winner's and seller's letters exactly once.

The store marks an auction `settled_in_game` when it is handed to the game, which then writes
the letters. These tests check that hand-off happens once and only for ended auctions."""
import asyncio
import httpx
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.infrastructure.database import MongoDB
from src.infrastructure import scheduler
from src.infrastructure.adapters.controllers.auction_controller import AuctionController
from src.domain.entities.auction import Auction


async def open_auction(auction_service, seller):
    return await auction_service.create_auction(
        seller.items[0].id, seller.id, datetime.now() + timedelta(hours=1))


@pytest.mark.asyncio
async def test_running_auction_is_not_pending_settlement(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    await open_auction(auction_service, seller)

    assert await auction_service.pending_settlements() == []
    assert await auction_service.settle_pending() == []


@pytest.mark.asyncio
async def test_ended_auction_is_finished_and_pending_settlement(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    pending = await auction_service.pending_settlements()

    assert [a.id for a in pending] == [auction.id]
    assert (await MongoDB.get_obj(Auction, auction.id)).rewarded is True


@pytest.mark.asyncio
async def test_settle_pending_hands_each_auction_over_once(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    first = await auction_service.settle_pending()
    second = await auction_service.settle_pending()

    assert [a.id for a in first] == [auction.id]
    assert first[0].settled_in_game is True
    assert second == []
    assert await auction_service.pending_settlements() == []


@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_simultaneous_settle_pending_hands_each_auction_over_once(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    results = await asyncio.gather(*(auction_service.settle_pending() for _ in range(5)))

    settled_ids = [a.id for batch in results for a in batch]
    assert settled_ids == [auction.id]


@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_claim_settled_succeeds_for_only_one_caller(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    claims = await asyncio.gather(*(auction_service.claim_settled(auction.id) for _ in range(5)))

    assert claims.count(True) == 1


@pytest.mark.asyncio
async def test_running_auction_cannot_be_settled(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)

    with pytest.raises(HTTPException) as error:
        await auction_service.mark_settled_in_game(auction.id)
    assert error.value.status_code == 400
    assert (await MongoDB.get_obj(Auction, auction.id)).settled_in_game is False


@pytest.mark.asyncio
async def test_auction_cannot_be_settled_twice(auction_service, auction_init_user, expire_auction):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)

    settled = await auction_service.mark_settled_in_game(auction.id)
    assert settled.settled_in_game is True and settled.rewarded is True

    with pytest.raises(HTTPException) as error:
        await auction_service.mark_settled_in_game(auction.id)
    assert error.value.status_code == 409


@pytest.mark.asyncio
async def test_unknown_auction_cannot_be_settled(auction_service):
    with pytest.raises(HTTPException) as error:
        await auction_service.mark_settled_in_game("no-such-auction")
    assert error.value.status_code == 404


# ---- settlement loop that pushes finished auctions to the game ----

def game_client(status_code: int, calls: list):
    async def handler(request: httpx.Request):
        calls.append(request)
        return httpx.Response(status_code, json={})
    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


@pytest.fixture
def broadcasts(monkeypatch):
    sent = []

    async def fake_broadcast(message):
        sent.append(message)
    monkeypatch.setattr(scheduler.auction_hub, "broadcast", fake_broadcast)
    return sent


@pytest.mark.asyncio
async def test_loop_marks_auction_settled_only_after_the_game_confirms(
        auction_service, auction_init_user, expire_auction, broadcasts):
    seller = await auction_init_user("seller")
    winner = await auction_init_user("winner")
    auction = await open_auction(auction_service, seller)
    await auction_service.make_bid(auction.id, winner.id, 200)
    await expire_auction(auction.id)
    calls = []

    async with game_client(201, calls) as client:
        await scheduler._refresh_once(auction_service, AuctionController(), client)

    assert len(calls) == 1
    assert calls[0].headers["X-Service-Token"] == scheduler.SERVICE_TOKEN
    payload = httpx.Response(200, content=calls[0].content).json()
    assert payload["id"] == auction.id
    assert payload["highest_bid"] == 200
    assert payload["highest_bidder"]["id"] == winner.id
    assert payload["user"]["id"] == seller.id
    assert (await MongoDB.get_obj(Auction, auction.id)).settled_in_game is True
    assert broadcasts == [{"type": "finished", "auction_id": auction.id}]


@pytest.mark.asyncio
async def test_loop_retries_when_the_game_rejects_the_settlement(
        auction_service, auction_init_user, expire_auction, broadcasts):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)
    failed_calls, ok_calls = [], []

    async with game_client(500, failed_calls) as client:
        await scheduler._refresh_once(auction_service, AuctionController(), client)
    assert (await MongoDB.get_obj(Auction, auction.id)).settled_in_game is False
    assert broadcasts == []

    async with game_client(200, ok_calls) as client:
        await scheduler._refresh_once(auction_service, AuctionController(), client)
    assert len(ok_calls) == 1
    assert (await MongoDB.get_obj(Auction, auction.id)).settled_in_game is True


@pytest.mark.asyncio
async def test_loop_does_not_push_a_settled_auction_again(
        auction_service, auction_init_user, expire_auction, broadcasts):
    seller = await auction_init_user("seller")
    auction = await open_auction(auction_service, seller)
    await expire_auction(auction.id)
    calls = []

    async with game_client(200, calls) as client:
        await scheduler._refresh_once(auction_service, AuctionController(), client)
        await scheduler._refresh_once(auction_service, AuctionController(), client)

    assert len(calls) == 1


@pytest.mark.asyncio
async def test_unreachable_game_counts_as_not_settled():
    async def handler(request):
        raise httpx.ConnectError("down")

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        assert await scheduler._notify_rol_game(client, {"id": "a1"}) is False

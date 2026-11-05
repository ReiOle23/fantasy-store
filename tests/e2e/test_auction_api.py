"""Business rule 15 end to end over HTTP: list, bid, live updates, ending and settlement."""
import pytest
import pytest_asyncio
import httpx
from datetime import datetime, timedelta

from main import app
from src.infrastructure.adapters.routes import auction_routes


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.fixture
def broadcasts(monkeypatch):
    sent = []

    async def fake_broadcast(message):
        sent.append(message)
    monkeypatch.setattr(auction_routes.auction_hub, "broadcast", fake_broadcast)
    return sent


async def hero(client, name, gold=1000, with_item=True):
    user = (await client.post("/register-user", json={"name": name, "password": "password123"})).json()
    await client.patch("/user-set-money", json={"user_id": user["id"], "user_token": user["token"], "amount": gold})
    item_id = None
    if with_item:
        item = await client.post("/user-add-item", json={
            "user_id": user["id"], "user_token": user["token"],
            "name": f"{name}'s sword", "price": 50, "item_type": "weapon",
        })
        item_id = item.json()["id"]
    return user, item_id


async def list_item(client, seller, item_id, starting_bid=None, hours=1):
    return await client.post("/auctions", json={
        "item_id": item_id, "user_id": seller["id"],
        "end_date": (datetime.now() + timedelta(hours=hours)).isoformat(),
        "starting_bid": starting_bid,
    })


async def bid(client, auction_id, user, price):
    return await client.post(f"/auctions/{auction_id}/bid",
                             json={"auction_id": auction_id, "user_id": user["id"], "price": price})


async def login(client, name):
    return (await client.post("/login-user", json={"name": name, "password": "password123"})).json()


@pytest.mark.asyncio
async def test_listing_takes_item_from_seller_and_uses_item_price(client, broadcasts):
    seller, item_id = await hero(client, "seller")

    response = await list_item(client, seller, item_id)

    assert response.status_code == 201
    auction = response.json()
    assert auction["highest_bid"] == 50
    assert auction["user"] == {"id": seller["id"], "name": "seller"}
    assert (await login(client, "seller"))["items"] == []


@pytest.mark.asyncio
async def test_listing_with_starting_price(client, broadcasts):
    seller, item_id = await hero(client, "seller")

    response = await list_item(client, seller, item_id, starting_bid=400)

    assert response.json()["highest_bid"] == 400


@pytest.mark.asyncio
async def test_listing_an_item_not_owned_is_rejected(client, broadcasts):
    seller, _ = await hero(client, "seller", with_item=False)
    _, other_item = await hero(client, "other")

    response = await list_item(client, seller, other_item)

    assert response.status_code == 404
    assert broadcasts == []


@pytest.mark.asyncio
async def test_auction_list_only_shows_running_auctions(client, broadcasts, expire_auction):
    seller, item_a = await hero(client, "seller")
    other, item_b = await hero(client, "other")
    running = (await list_item(client, seller, item_a)).json()
    ended = (await list_item(client, other, item_b)).json()
    await expire_auction(ended["id"])

    listed = (await client.get("/auctions")).json()

    assert [a["id"] for a in listed] == [running["id"]]


@pytest.mark.asyncio
async def test_bid_flow_over_http(client, broadcasts):
    seller, item_id = await hero(client, "seller")
    bidder, _ = await hero(client, "bidder", with_item=False)
    auction = (await list_item(client, seller, item_id)).json()

    too_low = await bid(client, auction["id"], bidder, 50)
    ok = await bid(client, auction["id"], bidder, 80)
    unaffordable = await bid(client, auction["id"], bidder, 5000)

    assert too_low.status_code == 404
    assert ok.status_code == 200 and ok.json() is True
    assert unaffordable.status_code == 404
    detail = (await client.get(f"/auction/{auction['id']}")).json()
    assert detail["highest_bid"] == 80
    assert detail["highest_bidder"] == {"id": bidder["id"], "name": "bidder"}
    assert [(b["user"]["name"], b["price"]) for b in detail["bids"]] == [("bidder", 80)]


@pytest.mark.asyncio
async def test_non_positive_bid_is_rejected(client, broadcasts):
    seller, item_id = await hero(client, "seller")
    bidder, _ = await hero(client, "bidder", with_item=False)
    auction = (await list_item(client, seller, item_id)).json()

    response = await bid(client, auction["id"], bidder, 0)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_watchers_are_told_about_new_auctions_and_bids(client, broadcasts):
    seller, item_id = await hero(client, "seller")
    bidder, _ = await hero(client, "bidder", with_item=False)

    auction = (await list_item(client, seller, item_id)).json()
    await bid(client, auction["id"], bidder, 10)  # rejected: too low
    await bid(client, auction["id"], bidder, 90)

    assert [m["type"] for m in broadcasts] == ["created", "bid"]
    assert broadcasts[0]["auction"]["id"] == auction["id"]
    assert broadcasts[1]["auction"]["highest_bid"] == 90
    assert broadcasts[1]["auction"]["highest_bidder"]["name"] == "bidder"


@pytest.mark.asyncio
async def test_ended_auction_delivers_item_and_gold(client, broadcasts, expire_auction):
    seller, item_id = await hero(client, "seller")
    bidder, _ = await hero(client, "bidder", with_item=False)
    auction = (await list_item(client, seller, item_id)).json()
    await bid(client, auction["id"], bidder, 300)
    await expire_auction(auction["id"])

    detail = (await client.get(f"/auction/{auction['id']}")).json()

    assert detail["rewarded"] is True
    winner = await login(client, "bidder")
    seller_now = await login(client, "seller")
    assert [i["id"] for i in winner["items"]] == [item_id]
    assert winner["money"] == 700
    assert seller_now["money"] == 1300
    assert seller_now["items"] == []


@pytest.mark.asyncio
async def test_unsold_auction_returns_item_to_seller(client, broadcasts, expire_auction):
    seller, item_id = await hero(client, "seller")
    auction = (await list_item(client, seller, item_id)).json()
    await expire_auction(auction["id"])

    await client.get(f"/auction/{auction['id']}")

    seller_now = await login(client, "seller")
    assert [i["id"] for i in seller_now["items"]] == [item_id]
    assert seller_now["money"] == 1000


@pytest.mark.asyncio
async def test_settlement_over_http_happens_once(client, broadcasts, expire_auction):
    seller, item_id = await hero(client, "seller")
    auction = (await list_item(client, seller, item_id)).json()

    assert (await client.post(f"/auctions/{auction['id']}/settle-game")).status_code == 400
    await expire_auction(auction["id"])

    first = await client.post("/auctions/settle-pending")
    second = await client.post("/auctions/settle-pending")
    again = await client.post(f"/auctions/{auction['id']}/settle-game")

    assert [a["id"] for a in first.json()] == [auction["id"]]
    assert second.json() == []
    assert again.status_code == 409


@pytest.mark.asyncio
async def test_unknown_auction_is_not_found(client):
    assert (await client.get("/auction/no-such-auction")).status_code == 404

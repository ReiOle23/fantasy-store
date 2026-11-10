"""Alchemy gemstones at the auction house (card DufVAnUu, AC13): a gem is listed as item type "gem"
and the auction keeps its kind, rarity and value for the winner."""
import pytest
import pytest_asyncio
import httpx
from datetime import datetime, timedelta

from main import app
from src.domain.entities.item import Item
from src.infrastructure.adapters.routes import auction_routes

RUBY_PROPERTIES = {"color": "red", "rarity": "rare", "stat": "damage", "value": 90, "obj_type": "gem"}


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


async def hero_with_gem(client, name, quantity=1):
    user = (await client.post("/register-user", json={"name": name, "password": "password123"})).json()
    gem = await client.post("/user-add-item", json={
        "user_id": user["id"], "user_token": user["token"],
        "name": "Ruby", "price": 200, "quantity": quantity, "item_type": "gem", "properties": RUBY_PROPERTIES,
    })
    return user, gem


def test_ac13_gems_can_be_auctioned():
    assert Item(name="Ruby", quantity=2, price=200, item_type="gem").is_auctionable() is True


@pytest.mark.asyncio
async def test_ac13_a_gem_is_listed_and_keeps_its_kind_rarity_and_value(client, broadcasts):
    seller, gem = await hero_with_gem(client, "gem seller", quantity=2)
    assert gem.status_code in (200, 201)

    response = await client.post("/auctions", json={
        "item_id": gem.json()["id"], "user_id": seller["id"],
        "end_date": (datetime.now() + timedelta(hours=1)).isoformat(), "starting_bid": 300,
    })

    assert response.status_code == 201
    listed = next(a for a in (await client.get("/auctions")).json() if a["id"] == response.json()["id"])
    assert listed["item"]["item_type"] == "gem"
    assert listed["item"]["quantity"] == 2
    assert {k: listed["item"]["properties"][k] for k in RUBY_PROPERTIES} == RUBY_PROPERTIES

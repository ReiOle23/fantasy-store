"""Business rules 2 and 15 end to end: unique hero names and limited-stock unique items."""
import pytest
import pytest_asyncio
import httpx

from main import app
from src.infrastructure.database import MongoDB
from src.domain.entities.item import Item


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def register(client, name, gold=0):
    user = (await client.post("/register-user", json={"name": name, "password": "password123"})).json()
    if gold:
        await client.patch("/user-set-money", json={"user_id": user["id"], "user_token": user["token"], "amount": gold})
    return user


async def buy(client, user, item_id, quantity=1):
    return await client.post("/buy-item", json={
        "item_id": item_id, "user_id": user["id"], "user_token": user["token"], "quantity": quantity})


@pytest.mark.asyncio
async def test_hero_name_is_unique(client):
    await register(client, "Aragorn")

    response = await client.post("/register-user", json={"name": "Aragorn", "password": "password123"})

    assert response.status_code == 404
    assert "exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_rename_to_a_taken_name_is_rejected(client):
    await register(client, "Aragorn")
    other = await register(client, "Boromir")

    response = await client.patch("/user-name", json={
        "user_id": other["id"], "user_token": other["token"], "name": "Aragorn"})

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_limited_item_sells_until_stock_runs_out(client):
    item = Item(name="Crown of Ash", quantity=2, price=100)
    await MongoDB.save_obj(item)
    first = await register(client, "first", gold=1000)
    second = await register(client, "second", gold=1000)

    assert (await buy(client, first, item.id)).status_code == 200
    assert (await client.get(f"/items/{item.id}")).json()["quantity"] == 1
    assert (await buy(client, second, item.id, quantity=2)).status_code == 404
    assert (await buy(client, second, item.id)).status_code == 200

    assert (await client.get(f"/items/{item.id}")).status_code == 404
    assert (await buy(client, first, item.id)).status_code == 404
    first_now = (await client.post("/login-user", json={"name": "first", "password": "password123"})).json()
    assert first_now["money"] == 900
    assert len(first_now["items"]) == 1


@pytest.mark.asyncio
async def test_buying_zero_units_is_rejected(client):
    item = Item(name="Crown of Ash", quantity=2, price=100)
    await MongoDB.save_obj(item)
    buyer = await register(client, "buyer", gold=1000)

    assert (await buy(client, buyer, item.id, quantity=0)).status_code == 422

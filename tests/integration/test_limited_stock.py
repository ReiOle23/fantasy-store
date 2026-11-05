"""Business rule 15 — unique items in limited quantity: when stock runs out, nobody else can buy."""
import asyncio
import pytest
from fastapi import HTTPException

from src.infrastructure.database import MongoDB
from src.domain.entities.item import Item
from src.domain.entities.user import User


async def rich_user(create_user, user_service, name, money=1000):
    user = await create_user(name)
    await user_service.add_money(user.id, user.token, money)
    return user


@pytest.mark.asyncio
async def test_buying_takes_price_times_quantity_and_lowers_stock(item_service, user_service, create_user, create_item):
    buyer = await rich_user(create_user, user_service, "buyer")
    item = await create_item("Crown of Ash", quantity=5, price=100)

    await item_service.buy_item(item.id, buyer.id, buyer.token, quantity=3)

    stored_buyer = await MongoDB.get_obj(User, buyer.id)
    assert stored_buyer.money == 700
    bought = next(i for i in stored_buyer.items if i.name == "Crown of Ash")
    assert bought.quantity == 3
    assert bought.owner == buyer.id
    assert bought.id != item.id
    assert (await MongoDB.get_obj(Item, item.id)).quantity == 2


@pytest.mark.asyncio
async def test_cannot_buy_more_than_the_stock_left(item_service, user_service, create_user, create_item):
    buyer = await rich_user(create_user, user_service, "buyer")
    item = await create_item("Crown of Ash", quantity=2, price=100)

    with pytest.raises(HTTPException) as error:
        await item_service.buy_item(item.id, buyer.id, buyer.token, quantity=3)
    assert "sold out" in error.value.detail

    stored_buyer = await MongoDB.get_obj(User, buyer.id)
    assert stored_buyer.money == 1000
    assert stored_buyer.items == []
    assert (await MongoDB.get_obj(Item, item.id)).quantity == 2


@pytest.mark.asyncio
async def test_unaffordable_purchase_keeps_stock_and_gold(item_service, user_service, create_user, create_item):
    buyer = await rich_user(create_user, user_service, "buyer", money=150)
    item = await create_item("Crown of Ash", quantity=5, price=100)

    with pytest.raises(HTTPException):
        await item_service.buy_item(item.id, buyer.id, buyer.token, quantity=2)

    assert (await MongoDB.get_obj(User, buyer.id)).money == 150
    assert (await MongoDB.get_obj(Item, item.id)).quantity == 5


@pytest.mark.asyncio
async def test_item_is_gone_from_market_when_last_unit_is_sold(item_service, user_service, create_user, create_item):
    first = await rich_user(create_user, user_service, "first")
    second = await rich_user(create_user, user_service, "second")
    item = await create_item("Crown of Ash", quantity=2, price=100)

    await item_service.buy_item(item.id, first.id, first.token, quantity=2)

    assert await item_service.get_by_id(item.id) is None
    assert all(i.id != item.id for i in await item_service.get_items())
    with pytest.raises(HTTPException):
        await item_service.buy_item(item.id, second.id, second.token)
    assert (await MongoDB.get_obj(User, second.id)).money == 1000


@pytest.mark.asyncio
async def test_item_owned_by_a_hero_cannot_be_bought_from_market(item_service, user_service, create_user):
    buyer = await rich_user(create_user, user_service, "buyer")
    owned = Item(name="Owned blade", quantity=1, price=10, owner="someone-else")
    await MongoDB.save_obj(owned)

    with pytest.raises(HTTPException) as error:
        await item_service.buy_item(owned.id, buyer.id, buyer.token)
    assert "owned" in error.value.detail


@pytest.mark.asyncio
async def test_purchase_with_wrong_token_is_rejected(item_service, user_service, create_user, create_item):
    buyer = await rich_user(create_user, user_service, "buyer")
    item = await create_item("Crown of Ash", quantity=1, price=100)

    with pytest.raises(HTTPException) as error:
        await item_service.buy_item(item.id, buyer.id, "not-the-token")
    assert "token" in error.value.detail
    assert (await MongoDB.get_obj(Item, item.id)).quantity == 1


@pytest.mark.repeat(10)
@pytest.mark.asyncio
async def test_many_buyers_at_once_get_exactly_the_stock_left(item_service, user_service, create_user, create_item):
    buyers = [await rich_user(create_user, user_service, f"user{i}") for i in range(10)]
    item = await create_item("Crown of Ash", quantity=3, price=100)

    results = await asyncio.gather(
        *(item_service.buy_item(item.id, b.id, b.token) for b in buyers),
        return_exceptions=True,
    )

    assert sum(not isinstance(r, Exception) for r in results) == 3
    assert await item_service.get_by_id(item.id) is None
    for buyer, result in zip(buyers, results):
        stored = await MongoDB.get_obj(User, buyer.id)
        if isinstance(result, Exception):
            assert stored.money == 1000 and stored.items == []
        else:
            assert stored.money == 900 and len(stored.items) == 1

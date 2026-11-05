"""Business rule 15 — listing an item."""
import asyncio
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.infrastructure.database import MongoDB
from src.domain.entities.auction import Auction
from src.domain.entities.item import Item
from src.domain.entities.user import User


def in_one_day():
    return datetime.now() + timedelta(hours=24)


@pytest.mark.asyncio
async def test_starting_price_defaults_to_item_price(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    item = seller.items[0]

    auction = await auction_service.create_auction(item.id, seller.id, in_one_day())

    assert auction.highest_bid == item.price
    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.highest_bid == item.price
    assert stored.highest_bidder is None


@pytest.mark.asyncio
async def test_seller_can_choose_starting_price(auction_service, auction_init_user):
    seller = await auction_init_user("seller")

    auction = await auction_service.create_auction(seller.items[0].id, seller.id, in_one_day(), starting_bid=300)

    assert auction.highest_bid == 300


@pytest.mark.asyncio
async def test_seller_chooses_the_auction_end(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    end = in_one_day()

    auction = await auction_service.create_auction(seller.items[0].id, seller.id, end)

    stored = await MongoDB.get_obj(Auction, auction.id)
    assert abs((stored.end_date - end).total_seconds()) < 1


@pytest.mark.asyncio
async def test_item_leaves_seller_inventory_while_auction_runs(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    item_id = seller.items[0].id

    auction = await auction_service.create_auction(item_id, seller.id, in_one_day())

    stored_seller = await MongoDB.get_obj(User, seller.id)
    assert stored_seller.get_item(item_id) is None
    stored = await MongoDB.get_obj(Auction, auction.id)
    assert stored.item.id == item_id


@pytest.mark.asyncio
async def test_listed_item_cannot_be_listed_again(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    item_id = seller.items[0].id
    await auction_service.create_auction(item_id, seller.id, in_one_day())

    with pytest.raises(HTTPException) as error:
        await auction_service.create_auction(item_id, seller.id, in_one_day())
    assert error.value.status_code == 404


@pytest.mark.repeat(5)
@pytest.mark.asyncio
async def test_same_item_listed_at_the_same_moment_ends_in_one_auction(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    item_id = seller.items[0].id

    results = await asyncio.gather(
        *(auction_service.create_auction(item_id, seller.id, in_one_day()) for _ in range(5)),
        return_exceptions=True,
    )

    assert sum(not isinstance(r, Exception) for r in results) == 1
    assert len(await MongoDB.get_all(Auction)) == 1


@pytest.mark.asyncio
async def test_seller_cannot_list_an_item_they_do_not_own(auction_service, auction_init_user):
    seller = await auction_init_user("seller")
    other = await auction_init_user("other")

    with pytest.raises(HTTPException) as error:
        await auction_service.create_auction(other.items[0].id, seller.id, in_one_day())
    assert error.value.status_code == 404
    assert await MongoDB.get_all(Auction) == []
    assert (await MongoDB.get_obj(User, other.id)).get_item(other.items[0].id) is not None


@pytest.mark.asyncio
async def test_unknown_seller_cannot_list(auction_service, auction_init_user):
    seller = await auction_init_user("seller")

    with pytest.raises(HTTPException) as error:
        await auction_service.create_auction(seller.items[0].id, "no-such-user", in_one_day())
    assert error.value.status_code == 404


@pytest.mark.asyncio
async def test_material_can_be_listed(auction_service, create_user):
    seller = await create_user("seller")
    material = Item.material(name="Iron ore", price=5, quantity=20)
    seller.add_item(material)
    await MongoDB.save_obj(seller)

    auction = await auction_service.create_auction(material.id, seller.id, in_one_day())

    assert auction.item.quantity == 20


@pytest.mark.asyncio
async def test_item_that_is_not_weapon_armour_or_material_cannot_be_listed(auction_service, create_user):
    seller = await create_user("seller")
    potion = Item(name="Health potion", price=5, quantity=1, item_type="potion")
    seller.add_item(potion)
    await MongoDB.save_obj(seller)

    with pytest.raises(HTTPException) as error:
        await auction_service.create_auction(potion.id, seller.id, in_one_day())
    assert error.value.status_code == 400
    assert (await MongoDB.get_obj(User, seller.id)).get_item(potion.id) is not None

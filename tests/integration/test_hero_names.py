"""Business rule 2: a hero name is unique in the whole world; it is how others see the hero in auctions."""
import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException

from src.infrastructure.adapters.controllers.auction_controller import AuctionController


@pytest.mark.asyncio
async def test_hero_cannot_take_a_name_already_in_use(user_service, create_user):
    await create_user("Aragorn")
    other = await create_user("Boromir")

    with pytest.raises(HTTPException) as error:
        await user_service.set_name(other.id, other.token, "Aragorn")
    assert error.value.status_code == 400


@pytest.mark.asyncio
async def test_hero_can_keep_their_own_name(user_service, create_user):
    hero = await create_user("Aragorn")

    renamed = await user_service.set_name(hero.id, hero.token, "Aragorn")

    assert renamed.name == "Aragorn"


@pytest.mark.asyncio
async def test_auctions_show_the_sellers_current_hero_name(auction_service, user_service, auction_init_user):
    seller = await auction_init_user("old-name")
    auction = await auction_service.create_auction(
        seller.items[0].id, seller.id, datetime.now() + timedelta(hours=1))
    await user_service.set_name(seller.id, seller.token, "new-name")

    listing = await AuctionController().get_auction(auction.id)

    assert listing.user.name == "new-name"

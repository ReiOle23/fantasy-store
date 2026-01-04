import asyncio, pytest
from src.infrastructure.database import MongoDB
from src.domain.entities.item import Item
from src.domain.entities.user import User

@pytest.mark.asyncio
async def test_all_items(item_service, create_item):
    await create_item()
    await create_item()
    await create_item()
    items = await item_service.get_items()
    assert len(items) == 3

@pytest.mark.asyncio
async def test_get_item(item_service, create_item):
    item = await create_item("unique_item")
    fetched = await item_service.get_by_id(item.id)
    assert fetched.id == item.id
    assert fetched.name == "unique_item"

@pytest.mark.asyncio
async def test_buy_unique_item_not_enought_money(item_service, create_user, create_item):
    user = await create_user("buyer")
    item = await create_item("splendid_item", 1, 100)
    assert user.has_item(item.name) is False
    with pytest.raises(Exception):
        await item_service.buy_item(item.id, user.id, user.token)

@pytest.mark.asyncio
async def test_buy_unique_item(item_service, user_service, create_user, create_item):
    user = await create_user("buyer")
    await user_service.add_money(user.id, user.token, 1000)
    item = await create_item("splendid_item", 1, 100)
    assert user.has_item(item.name) is False
    await item_service.buy_item(item.id, user.id, user.token)
    updated_user = await MongoDB.get_obj(User, user.id)
    assert updated_user.has_item(item.name) is True
    assert await MongoDB.get_obj(Item, item.id) == None

    with pytest.raises(Exception):
        await item_service.buy_item(item.id, user.id, user.token)

@pytest.mark.asyncio
async def test_buy_item_3_times(item_service, user_service, create_user, create_item):
    user = await create_user("buyer")
    await user_service.add_money(user.id, user.token, 1000)
    
    item = await create_item("splendid_item", 5, 100)
    await item_service.buy_item(item.id, user.id, user.token)
    await item_service.buy_item(item.id, user.id, user.token, quantity=2)
    await item_service.buy_item(item.id, user.id, user.token, quantity=1)
    
    updated_user = await MongoDB.get_obj(User, user.id)
    assert len(updated_user.items) == 3

@pytest.mark.asyncio
async def test_three_users_buy_same_item(item_service, user_service, create_user, create_item):
    users = [await create_user(f"user{i}") for i in range(3)]
    assert len(users) == 3
    for u in users:
        await user_service.add_money(u.id, u.token, 1000)
        
    item = await create_item("splendid_item", 1, 200)
    # tasks = [asyncio.create_task(item_service.buy_item(item.id, u.id, u.token)) for u in users]
    # results = await asyncio.gather(*tasks, return_exceptions=True)

    # successes = [r for r in results if not isinstance(r, Exception)]
    # failures = [r for r in results if isinstance(r, Exception)]

    # assert len(successes) == 1
    # assert all(isinstance(e, ValueError) for e in failures)

    # final = await item_service.get_by_id(item.id)
    # assert final.owner == successes[0].owner

@pytest.mark.skip(reason="Needs money implementation in User entity")
@pytest.mark.asyncio
async def test_three_users_buy_different_items(item_service, create_user, create_item):
    users = [create_user(f"user{i}") for i in range(3)]
    items = [create_item() for _ in range(3)]
    tasks = [asyncio.create_task(item_service.buy_item(it.id, u.id, u.token)) for it, u in zip(items, users)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    assert all(not isinstance(r, Exception) for r in results)

    for it, u in zip(items, users):
        final = item_service.get_by_id(it.id)
        assert final.owner == u.id
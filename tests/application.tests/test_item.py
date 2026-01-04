from src.application.adapters.item_service import ItemService
from src.application.adapters.user_service import UserService
from src.infrastructure.database import Database
from src.domain.entities.item import Item
from pytest import fixture
import pytest
import asyncio

@fixture
def testuser():
    user_service = UserService()
    return user_service.create("testuser", "password123")

@fixture
def testuser2():
    user_service = UserService()
    return user_service.create("testuser2", "password123")

@fixture
def testuser3():
    user_service = UserService()
    return user_service.create("testuser3", "password123")

@fixture
def items():
    item_service = ItemService()
    items = Database.get_all(Item)[:3]
    return [item_service.get_by_id(i.id) for i in items]

def test_all_items(): 
    item_service = ItemService()
    items = item_service.get_items()
    assert len(Database.get_all(Item)) == len(items)
    
def test_get_item():
    item_service = ItemService()
    item = Database.get_all(Item)[0]
    assert Database.get_obj(Item, item.id) == item_service.get_by_id(item.id)

@pytest.mark.asyncio
async def test_buy_item(testuser):
    item_service = ItemService()
    item = Database.get_all(Item)[0]
    assert item.owner is None
    await item_service.buy_item(item.id, testuser.id, testuser.token)
    item = Database.get_obj(Item, item.id)
    assert item.owner.id == testuser.id

@pytest.mark.asyncio
async def test_three_users_buy_same_item(items, testuser, testuser2, testuser3):
    item_service = ItemService()
    tasks = [
        asyncio.create_task(item_service.buy_item(items[0].id, u.id, u.token))
        for u in (testuser, testuser2, testuser3)
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    successes = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]

    assert len(successes) == 1
    assert len(errors) == 2

    final_item = Database.get_obj(Item, items[0].id)
    assert final_item.owner.id == successes[0].owner.id

@pytest.mark.asyncio
async def test_three_users_buy_different_items(items, testuser, testuser2, testuser3):
    item_service = ItemService()
    tasks = [
        asyncio.create_task(item_service.buy_item(iu[0].id, iu[1].id, iu[1].token))
        for iu in zip(items, [testuser, testuser2, testuser3])
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    successes = [r for r in results if not isinstance(r, Exception)]
    errors = [r for r in results if isinstance(r, Exception)]

    assert len(successes) == 3
    assert len(errors) == 0

    final_item = Database.get_obj(Item, items[0].id)
    assert final_item.owner.id == successes[0].owner.id
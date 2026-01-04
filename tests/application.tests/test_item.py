from src.application.adapters.item_service import ItemService
from src.application.adapters.user_service import UserService
from src.infrastructure.database import Database
from src.domain.entities.item import Item
from pytest import fixture

@fixture
def testuser():
    user_service = UserService()
    return user_service.create("testuser", "password123")

@fixture
def testuser2():
    user_service = UserService()
    return user_service.create("testuser2", "password123")

def test_all_items(): 
    item_service = ItemService()
    items = item_service.get_items()
    assert len(Database.get_all(Item)) == len(items)
    
def test_get_item():
    item_service = ItemService()
    item_id = Database.get_all(Item)[0]
    assert Database.get_obj(Item, item_id) == item_service.get_by_id(item_id)
    
def test_buy_item(testuser):
    item_service = ItemService()
    item = Database.get_all(Item)[0]
    assert item.owner is None
    item_service.buy_item(item.id, testuser.id, testuser.token)
    item = Database.get_obj(Item, item.id)
    assert item.owner == testuser
    
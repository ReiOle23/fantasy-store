import pytest, pytest_asyncio, uuid
from src.infrastructure.database import MongoDB
from src.application.adapters.user_service import UserService
from src.application.adapters.item_service import ItemService
from src.domain.entities.item import Item

@pytest_asyncio.fixture(autouse=True)
async def setup_test_database():
    """Automatically setup and cleanup database for all tests"""
    with MongoDB.using_database("fantasy_back_test"):
        await MongoDB.clear()
        yield
        await MongoDB.clear()
        await MongoDB.disconnect()
        
@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def item_service():
    return ItemService()

@pytest_asyncio.fixture
async def create_user(user_service):
    """Fixture to create users in tests"""
    async def _create(name: str):
        return await user_service.create(name, "password123")
    return _create

@pytest_asyncio.fixture
async def create_item():
    """Fixture to create items in tests"""
    async def _create(name: str | None = None, quantity: int = 1, price: int = 10):
        item = Item(
            id=str(uuid.uuid4()), 
            name=name or f"item-{uuid.uuid4()}", 
            owner=None, 
            quantity=quantity, 
            price=price
        )
        await MongoDB.save_obj(item)
        return item
    return _create
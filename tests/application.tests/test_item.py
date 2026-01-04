import uuid, asyncio, pytest
from src.application.adapters.item_service import ItemService
from src.application.adapters.user_service import UserService
from src.infrastructure.database import Database
from src.domain.entities.item import Item

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def item_service():
    return ItemService()

@pytest.fixture
def create_user(user_service):
    def _create(name: str):
        return user_service.create(name, "password123")
    return _create

@pytest.fixture
def create_item():
    def _create(name: str | None = None, quantity: int = 1, price: int = 10):
        item = Item(id=str(uuid.uuid4()), name=name or f"item-{uuid.uuid4()}", owner=None, quantity=quantity, price=price)
        Database.save_obj(item)
        return item
    return _create

def test_all_items(item_service, create_item):
    # explicit setup
    create_item()
    create_item()
    create_item()
    items = item_service.get_items()
    assert len(items) == 3

def test_get_item(item_service, create_item):
    item = create_item("unique_item")
    fetched = item_service.get_by_id(item.id)
    assert fetched.id == item.id
    assert fetched.name == "unique_item"

@pytest.mark.asyncio
async def test_buy_item(item_service, create_user, create_item):
    user = create_user("buyer")
    item = create_item()
    assert item.owner is None
    bought = await item_service.buy_item(item.id, user.id, user.token)
    assert bought.owner.id == user.id

    with pytest.raises(ValueError):
        await item_service.buy_item(item.id, user.id, user.token)

@pytest.mark.asyncio
async def test_three_users_buy_same_item(item_service, create_user, create_item):
    users = [create_user(f"user{i}") for i in range(3)]
    item = create_item()
    tasks = [asyncio.create_task(item_service.buy_item(item.id, u.id, u.token)) for u in users]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]

    assert len(successes) == 1
    assert all(isinstance(e, ValueError) for e in failures)

    final = item_service.get_by_id(item.id)
    assert final.owner.id == successes[0].owner.id

@pytest.mark.asyncio
async def test_three_users_buy_different_items(item_service, create_user, create_item):
    users = [create_user(f"user{i}") for i in range(3)]
    items = [create_item() for _ in range(3)]
    tasks = [asyncio.create_task(item_service.buy_item(it.id, u.id, u.token)) for it, u in zip(items, users)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    assert all(not isinstance(r, Exception) for r in results)

    for it, u in zip(items, users):
        final = item_service.get_by_id(it.id)
        assert final.owner.id == u.id
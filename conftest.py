import pytest
from src.infrastructure.database import Database

@pytest.fixture(scope="function", autouse=True)
def use_test_database():
    """Use test database for all tests"""
    with Database.using_database('database_test.json'):
        Database.clear()
        Database.save_multiple_obj("Item",
                {
            "a1b2c3d4-e5f6-7890-abcd-ef1234567890": {
                "name": "Elven Bow of the Woodland Realm",
                "quantity": 15,
                "price": 850,
                "owner": None,
                "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            },
            "b2c3d4e5-f6a7-8901-bcde-f12345678901": {
                "name": "Mithril Chain Mail",
                "quantity": 8,
                "price": 2500,
                "owner": None,
                "id": "b2c3d4e5-f6a7-8901-bcde-f12345678901"
            },
            "c3d4e5f6-a7b8-9012-cdef-123456789012": {
                "name": "Sword of the Witch-king",
                "quantity": 3,
                "price": 3200,
                "owner": None,
                "id": "c3d4e5f6-a7b8-9012-cdef-123456789012"
            },
            "d4e5f6a7-b8c9-0123-def1-234567890123": {
                "name": "Staff of Gandalf the Grey",
                "quantity": 2,
                "price": 5000,
                "owner": None,
                "id": "d4e5f6a7-b8c9-0123-def1-234567890123"
            },
            "e5f6a7b8-c9d0-1234-ef12-345678901234": {
                "name": "Orcish Battle Axe",
                "quantity": 25,
                "price": 450,
                "owner": None,
                "id": "e5f6a7b8-c9d0-1234-ef12-345678901234"
            },
            "f6a7b8c9-d0e1-2345-f123-456789012345": {
                "name": "Dwarven War Hammer",
                "quantity": 12,
                "price": 780,
                "owner": None,
                "id": "f6a7b8c9-d0e1-2345-f123-456789012345"
            },
            "a7b8c9d0-e1f2-3456-1234-567890123456": {
                "name": "Ring of Invisibility",
                "quantity": 1,
                "price": 10000,
                "owner": None,
                "id": "a7b8c9d0-e1f2-3456-1234-567890123456"
            },
            "b8c9d0e1-f2a3-4567-2345-678901234567": {
                "name": "Palantír Seeing Stone",
                "quantity": 2,
                "price": 8500,
                "owner": None,
                "id": "b8c9d0e1-f2a3-4567-2345-678901234567"
            },
            "c9d0e1f2-a3b4-5678-3456-789012345678": {
                "name": "Cloak of Lórien",
                "quantity": 20,
                "price": 650,
                "owner": None,
                "id": "c9d0e1f2-a3b4-5678-3456-789012345678"
            }
        })
        yield
        
import pytest
from src.infrastructure.database import Database

@pytest.fixture(scope="function", autouse=True)
def use_test_database():
    """Use test database for all tests"""
    with Database.using_database('database_test.json'):
        Database.clear()
        yield
        
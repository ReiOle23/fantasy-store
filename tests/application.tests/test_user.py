from src.application.adapters.user_service import UserService
from pytest import fixture

@fixture
def testuser():
    user_service = UserService()
    return user_service.create("testuser", "password123")

def test_user_create(testuser):
    assert testuser["name"] == "testuser"
    
def test_user_login(testuser):
    user_service = UserService()
    new_user = user_service.login("testuser", "password123")
    assert testuser == new_user
    
def test_user_login_invalid_credentials():
    user_service = UserService()
    try:
        user_service.login("testuser", "wrongpassword")
        assert False, "Expected ValueError"
    except ValueError as e:
        assert str(e) == "Invalid credentials"
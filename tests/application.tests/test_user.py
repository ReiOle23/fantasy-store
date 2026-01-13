import pytest

@pytest.mark.asyncio
async def test_user_create(user_service):
    testuser = await user_service.create("testuser", "password123")
    assert testuser.name == "testuser"
    
@pytest.mark.asyncio
async def test_user_create_duplicate(user_service):
    await user_service.create("testuser", "password123")
    with pytest.raises(Exception):
        await user_service.create("testuser", "password123")
    
@pytest.mark.asyncio
async def test_user_login(user_service):
    testuser = await user_service.create("testuser", "password123")
    new_user = await user_service.login("testuser", "password123")
    assert testuser == new_user

@pytest.mark.asyncio
async def test_user_login_invalid_credentials(user_service):
    with pytest.raises(Exception, match="Invalid credentials"):
        await user_service.login("testuser", "wrongpassword")
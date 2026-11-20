"""Card w0mvlKgp "Game not optimized for mobile, android." (crown-trade-front spec
docs/acceptance/w0mvlKgp-game-not-optimized-for-mobile-android.txt): the Android app runs
on the origin https://localhost and calls this API cross-origin."""
import httpx
import pytest
import pytest_asyncio

from main import app


@pytest_asyncio.fixture
async def client():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as c:
        yield c


async def preflight(client, origin):
    return await client.options("/items", headers={
        "Origin": origin,
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "authorization,content-type",
    })


@pytest.mark.asyncio
async def test_ac13_the_android_app_origin_is_allowed(client):
    response = await preflight(client, "https://localhost")

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "https://localhost"


@pytest.mark.asyncio
@pytest.mark.parametrize("origin", [
    "https://crownandtrade.com",
    "https://www.crownandtrade.com",
    "http://localhost:8100",
])
async def test_ac13_the_existing_origins_are_still_allowed(client, origin):
    response = await preflight(client, origin)

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin


@pytest.mark.asyncio
async def test_ac13_an_unknown_origin_is_not_allowed(client):
    response = await preflight(client, "https://evil.example.com")

    assert response.headers.get("access-control-allow-origin") is None

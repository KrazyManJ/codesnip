from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)


@pytest.mark.asyncio
async def test_get_valid_snippet_by_id():
    snippet_id = "6911c38853ed167b0b3cf306"
    response = await async_client.get(f"/snippets/{snippet_id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_invalid_id():
    response = await async_client.get("/snippets/random_thing_that_is_not_id")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_unknown_id():
    snippet_id = "691139572bb41dcaba909a65"
    response = await async_client.get(f"/snippets/{snippet_id}")
    assert response.status_code == 404
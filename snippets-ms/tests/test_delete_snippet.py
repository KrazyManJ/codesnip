from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)

@pytest.mark.asyncio
async def test_delete_success():
    snippet_id = "6911c38853ed167b0b3cf306"
    result = await async_client.delete(f"/snippets/{snippet_id}")
    assert result.status_code == 204
    list_result = await async_client.get("/snippets")
    assert len(list_result.json()) == 1


@pytest.mark.asyncio
async def test_update_invalid_id():
    response = await async_client.delete("/snippets/random_thing_that_is_not_id")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_unknown_id():
    snippet_id = "691139572bb41dcaba909a65"
    response = await async_client.delete(f"/snippets/{snippet_id}")
    assert response.status_code == 404
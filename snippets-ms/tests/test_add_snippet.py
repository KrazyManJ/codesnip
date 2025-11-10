from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)

@pytest.mark.asyncio
async def test_add_success():
    response = await async_client.post("/snippets", json={
        "title": "New snippet",
        "description": "Description",
        "code": "async def func()",
        "language": "Python"
    })
    assert response.status_code == 201

    all_snippets_response = await async_client.get("/snippets")
    assert len(all_snippets_response.json()) == 3


@pytest.mark.asyncio
async def test_add_invalid_body():
    response = await async_client.post("/snippets", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_remove_obsolette_key():
    response = await async_client.post("/snippets", json={
        "title": "New snippet",
        "description": "Description",
        "code": "async def func()",
        "language": "Python",
        "random_key": "random_value"
    })
    assert response.status_code == 201
    assert "random_key" not in response.json()
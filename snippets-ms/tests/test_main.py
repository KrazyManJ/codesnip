from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
import pytest
from app.main import app

client = TestClient(app)


def test_read_items():
    response = client.get("/snippets")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_get_invalid_id():
    response = client.get("/snippets/random_thing_that_is_not_id")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid format of snippet id"


@pytest.mark.asyncio
async def test_get_unknown_id():
    snippet_id = "691139572bb41dcaba909a65"
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get(f"/snippets/{snippet_id}")
        assert response.status_code == 404
        assert response.json()[
            "detail"] == f"Snippet with id '{snippet_id}' not found"

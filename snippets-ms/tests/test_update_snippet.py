import pytest


@pytest.mark.asyncio
async def test_update_success(async_client):
    snippet_id = "6911c38853ed167b0b3cf306"
    snippet = (await async_client.get(f"/snippets/{snippet_id}")).json()
    assert snippet["title"] != "New title"
    snippet["title"] = "New title"

    response = await async_client.put(f"/snippets/{snippet_id}", json=snippet)
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


@pytest.mark.asyncio
async def test_update_invalid_body(async_client):
    snippet_id = "6911c38853ed167b0b3cf306"
    response = await async_client.put(f"/snippets/{snippet_id}", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_invalid_id(async_client):
    response = await async_client.put("/snippets/random_thing_that_is_not_id", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_update_unknown_id(async_client):
    snippet_id = "691139572bb41dcaba909a65"
    response = await async_client.put(f"/snippets/{snippet_id}", json={})
    assert response.status_code == 404
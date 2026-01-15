import pytest


@pytest.mark.asyncio
async def test_get_valid_snippet_by_id(async_client):
    snippet_id = "6911c38853ed167b0b3cf306"
    response = await async_client.get(f"/snippets/{snippet_id}")
    assert response.status_code == 200
    

@pytest.mark.asyncio
async def test_get_invalid_private_to_user(async_client):
    snippet_id = "696843588e0bf4375c065efd"
    response = await async_client.get(f"/snippets/{snippet_id}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_invalid_id(async_client):
    response = await async_client.get("/snippets/random_thing_that_is_not_id")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_unknown_id(async_client):
    snippet_id = "691139572bb41dcaba909a65"
    response = await async_client.get(f"/snippets/{snippet_id}")
    assert response.status_code == 404
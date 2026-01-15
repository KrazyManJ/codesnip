import pytest


@pytest.mark.asyncio
async def test_me_success(async_client):
    response = await async_client.get("/saves/me")
    assert response.status_code == 200
    json = response.json()
    assert type(json) == dict
    assert len(json["items"]) == 2


@pytest.mark.asyncio
async def test_me_failure_unauthenticated(async_client, unauthenticated):
    response = await async_client.get("/saves/me")
    assert response.status_code == 401

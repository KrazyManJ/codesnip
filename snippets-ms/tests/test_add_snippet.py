import pytest

@pytest.mark.asyncio
async def test_add_success(async_client):
    response = await async_client.post("/snippets", json={
        "title": "New snippet",
        "description": "Description",
        "code": "async def func()",
        "language": "Python"
    })
    assert response.status_code == 201

    all_snippets_response = await async_client.get("/snippets")
    assert len(all_snippets_response.json()["items"]) == 3


@pytest.mark.asyncio
async def test_add_invalid_body(async_client):
    response = await async_client.post("/snippets", json={})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_remove_obsolete_key(async_client):
    response = await async_client.post("/snippets", json={
        "title": "New snippet",
        "description": "Description",
        "code": "async def func()",
        "language": "Python",
        "random_key": "random_value"
    })
    assert response.status_code == 201
    assert "random_key" not in response.json()
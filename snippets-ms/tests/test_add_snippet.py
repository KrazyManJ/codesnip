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
    
    
@pytest.mark.asyncio
async def test_add_unauthorized(async_client, unauthenticated):
    response = await async_client.post("/snippets", json={
        "title": "New snippet",
        "description": "Description",
        "code": "async def func()",
        "language": "Python"
    })
    assert response.status_code == 401
    

@pytest.mark.asyncio
async def test_add_empty_strings(async_client):
    snippet = {
        "title": "New snippet",
        "description": "Description",
        "code": "async def func()",
        "language": "Python"
    }
    valid_empty_keys = ["description"]
    for key in [k for k in snippet.keys() if k not in valid_empty_keys]:
        tweaked_snippet = snippet.copy()
        tweaked_snippet[key] = ""
        response = await async_client.post("/snippets", json=tweaked_snippet)
        assert response.status_code == 422
import pytest


@pytest.mark.asyncio
async def test_save_success(async_client):
    response = await async_client.post(
        url="/saves",
        json={"snippet_id": "6968f448f27ed64302bdcf50"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert "snippet_id" in response_json
    assert "created_at" in response_json
    
    
@pytest.mark.asyncio
async def test_save_fail_unauthenticated(async_client, unauthenticated):
    response = await async_client.post(
        url="/saves",
        json={"snippet_id": "6968f448f27ed64302bdcf50"}
    )
    assert response.status_code == 401
    
    
@pytest.mark.asyncio
async def test_save_fail_invalid_body(async_client):
    response = await async_client.post("/saves", json={})
    assert response.status_code == 422
    
    
@pytest.mark.asyncio
async def test_save_fail_invalid_id(async_client):
    response = await async_client.post("/saves", json={
        "snippet_id": "abcd"
    })
    assert response.status_code == 422
    

@pytest.mark.asyncio
async def test_save_fail_already_saved(async_client):
    await async_client.post(
        url="/saves",
        json={"snippet_id": "6968f448f27ed64302bdcf50"}
    )
    response = await async_client.post(
        url="/saves",
        json={"snippet_id": "6968f448f27ed64302bdcf50"}
    )
    assert response.status_code == 403

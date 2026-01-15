import pytest
import pytest_asyncio
from bson import ObjectId

SAVES = [str(ObjectId()) for _ in range(10) ]


@pytest_asyncio.fixture
async def init_with_save(async_client):
    for i in [1,3,7]:
        await async_client.post(
            url="/saves",
            json={"snippet_id": SAVES[i]}
        )
        
        
@pytest.mark.asyncio
async def test_check_status_success(async_client, init_with_save):
    response = await async_client.post("/saves/check-status", json={
        "snippet_ids": SAVES
    })
    assert response.status_code == 200
    json = response.json()
    assert type(json) is list
    assert len(json) == 3
    
    
@pytest.mark.asyncio
async def test_check_status_failure_unauthenticated(async_client, init_with_save, unauthenticated):
    response = await async_client.post("/saves/check-status", json={
        "snippet_ids": SAVES
    })
    assert response.status_code == 401
    

@pytest.mark.asyncio
async def test_check_status_failure_to_many_in_list(async_client, init_with_save):
    response = await async_client.post("/saves/check-status", json={
        "snippet_ids": [str(ObjectId()) for _ in range(101) ]
    })
    assert response.status_code == 422
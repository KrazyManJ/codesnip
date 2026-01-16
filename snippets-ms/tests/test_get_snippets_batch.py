import pytest
from bson import ObjectId

@pytest.mark.asyncio
async def test_get_batch_snippets_success(async_client):
    response = await async_client.post("/snippets/batch",json={
        "snippet_ids": [
            "6911c38853ed167b0b3cf306",
            "6911c4059f5ace328a43261b",
            "696843588e0bf4375c065efd" # PRIVATE, WONT BE RETURNED
        ]
    })
    assert response.status_code == 200
    json = response.json()
    assert type(json) == list
    assert len(json) == 2
    
@pytest.mark.asyncio
async def test_get_batch_snippets_fail_to_much(async_client):
    response = await async_client.post("/snippets/batch",json={
        "snippet_ids": [str(ObjectId()) for _ in range(101)],
    })
    assert response.status_code == 422
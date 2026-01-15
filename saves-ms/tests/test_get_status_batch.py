from datetime import datetime

import pytest
import pytest_asyncio
from bson import ObjectId

SNIPPETS_IDS = [str(ObjectId()) for _ in range(10)]

@pytest_asyncio.fixture
async def init_with_save(db_client):
    for snippet_id in SNIPPETS_IDS:
        await db_client["codesnip"]["saves"].insert_many(
            [
                {
                    "snippet_id": snippet_id, 
                    "user_id": str(ObjectId()),
                    "saved_at": datetime.now().isoformat(),
                } for _ in range(10)
            ]
        )

@pytest.mark.asyncio
async def test_get_status_batch_success(async_client, init_with_save):
    response = await async_client.post("/saves/stats/batch", json={
        "snippet_ids": SNIPPETS_IDS,
    })
    assert response.status_code == 200
    json = response.json()
    assert type(json) is list
    assert len(json) == 10
    first = json[0]
    assert "snippet_id" in first
    assert "stats" in first
    stats = first["stats"]
    assert "save_count" in stats
    assert stats["save_count"] == 10
    

@pytest.mark.asyncio
async def test_get_status_batch_empty(async_client):
    response = await async_client.post("/saves/stats/batch", json={
        "snippet_ids": SNIPPETS_IDS,
    })
    assert response.status_code == 200
    json = response.json()
    assert type(json) is list
    assert len(json) == 0
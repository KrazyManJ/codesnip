from datetime import datetime

import pytest
import pytest_asyncio
from bson import ObjectId

SNIPPET_ID = "6968f448f27ed64302bdcf50"

@pytest_asyncio.fixture
async def init_with_save(db_client):
    await db_client["codesnip"]["saves"].insert_many(
        [
            {
                "snippet_id": SNIPPET_ID, 
                "user_id": str(ObjectId()),
                "saved_at": datetime.now().isoformat(),
            } for _ in range(10)
        ]
    )


@pytest.mark.asyncio
async def test_get_stats_success(async_client, init_with_save):
    response = await async_client.get(f"/saves/{SNIPPET_ID}/stats")
    assert response.status_code == 200
    json = response.json()
    assert type(json) == dict
    assert "save_count" in json
    assert json["save_count"] == 10
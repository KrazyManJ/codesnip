import pytest
import pytest_asyncio

SNIPPET_ID = "6968f448f27ed64302bdcf50"

@pytest_asyncio.fixture
async def init_with_save(async_client):
    await async_client.post(
        url="/saves",
        json={"snippet_id": SNIPPET_ID}
    )

@pytest.mark.asyncio
async def test_get_save_success(async_client, init_with_save):
    response = await async_client.get(f"/saves/{SNIPPET_ID}")
    assert response.status_code == 200
    json = response.json()
    assert "snippet_id" in json
    assert "saved_at" in json
    assert json["snippet_id"] == SNIPPET_ID
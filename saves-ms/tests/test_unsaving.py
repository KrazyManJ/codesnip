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
async def test_unsave_success(async_client, init_with_save):
    response = await async_client.delete(f"/saves/{SNIPPET_ID}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_unsave_failure_does_not_exist(async_client, init_with_save):
    valid_not_existing_id = "6968ff23212c3f1b00b0a298"
    response = await async_client.delete(f"/saves/{valid_not_existing_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unsave_fail_unauthenticated(async_client, init_with_save, unauthenticated):
    response = await async_client.delete(f"/saves/{SNIPPET_ID}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unsave_fail_invalid_id(async_client, init_with_save):
    response = await async_client.delete("/saves/abcd")
    assert response.status_code == 422
import pytest


@pytest.mark.asyncio
async def test_get_langs_success(async_client):

    def list_diff(l1,l2): return [a for a,b in zip(l1, l2) if a==b] 

    result = await async_client.get("/langs")
    assert result.status_code == 200
    assert len(list_diff(result.json(), ["Python", "Java"])) == 0
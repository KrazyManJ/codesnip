from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)


@pytest.mark.asyncio
async def test_get_langs_success():

    def list_diff(l1,l2): return [a for a,b in zip(l1, l2) if a==b] 

    result = await async_client.get("/langs")
    assert result.status_code == 200
    assert len(list_diff(result.json(), ["Python", "Java"])) == 0
from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)


@pytest.mark.asyncio
async def test_get_stats_success():
    result = await async_client.get("/stats")
    assert result.status_code == 200
    stats = result.json()
    assert "total_snippets_count" in stats
    assert "total_bytes" in stats
    assert "languages_data" in stats
    assert len(stats["languages_data"]) == 2
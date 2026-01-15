import pytest


@pytest.mark.asyncio
async def test_get_stats_success(async_client):
    result = await async_client.get("/stats")
    assert result.status_code == 200
    stats = result.json()
    assert "total_snippets_count" in stats
    assert "total_bytes" in stats
    assert "languages_data" in stats
    assert len(stats["languages_data"]) == 2
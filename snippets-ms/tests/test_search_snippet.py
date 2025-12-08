import json
from httpx import ASGITransport, AsyncClient
import pytest

from app.main import app

async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)


@pytest.mark.asyncio
async def test_without_params_success():
    result = await async_client.post("/search")
    assert result.status_code == 200
    assert len(result.json()) == 2


@pytest.mark.asyncio
async def test_with_query_param_success():
    result = await async_client.post("/search?query=method,")
    assert result.status_code == 200
    assert result.json()[0]["title"] == "Main <b>method</b>"


@pytest.mark.asyncio
async def test_with_language_param_success():
    result = await async_client.post("/search?lang=python")
    print(json.dumps(result.json(),indent=4))
    assert result.status_code == 200
    assert result.json()[0]["title"] == "Lambda expression"


@pytest.mark.asyncio
async def test_with_language_query_param_success():
    result = await async_client.post("/search?query=method,&lang=Java")
    assert result.status_code == 200
    assert result.json()[0]["title"] == "Main <b>method</b>"


@pytest.mark.asyncio
async def test_search_empty():
    result = await async_client.post("/search?query=Closure,lang=Python")
    assert result.status_code == 200
    assert len(result.json()) == 0


@pytest.mark.asyncio
async def test_language_case_insensitivity():
    result = await async_client.post("/search?lang=pYtHoN")
    assert result.status_code == 200
    assert result.json()[0]["title"] == "Lambda expression"

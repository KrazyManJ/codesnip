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
    data = result.json()
    assert len(data) == 2
    first_result = data[0]
    
    assert "snippet" in first_result
    assert "id" in first_result["snippet"]
    assert "title" in first_result["snippet"]
    assert "language" in first_result["snippet"]
    
    assert "match" in first_result
    assert first_result["match"]["title"] == ""
    assert first_result["match"]["description"] != ""
    assert first_result["match"]["code"] == ""


@pytest.mark.asyncio
async def test_with_query_param_success():
    result = await async_client.post("/search?query=method,")
    assert result.status_code == 200
    data = result.json()
    assert len(data) == 1
    first_result = data[0]
    assert first_result["match"]["title"] == "Main <{%HL_START%}>method<{%HL_END%}>"


@pytest.mark.asyncio
async def test_with_language_param_success():
    result = await async_client.post("/search?lang=python")
    assert result.status_code == 200
    data = result.json()
    assert len(data) == 1
    first_result = data[0]
    assert first_result["snippet"]["title"] == "Lambda expression"
    assert first_result["match"]["title"] == ""


@pytest.mark.asyncio
async def test_with_language_query_param_success():
    result = await async_client.post("/search?query=method,&lang=Java")
    assert result.status_code == 200
    data = result.json()
    assert len(data) == 1
    first_result = data[0]
    assert first_result["snippet"]["title"] == "Main method"
    assert first_result["match"]["title"] == "Main <{%HL_START%}>method<{%HL_END%}>"


@pytest.mark.asyncio
async def test_search_empty():
    result = await async_client.post("/search?query=Closure,lang=Python")
    assert result.status_code == 200
    assert len(result.json()) == 0


@pytest.mark.asyncio
async def test_language_case_insensitivity():
    result = await async_client.post("/search?lang=pYtHoN")
    assert result.status_code == 200
    data = result.json()
    assert len(data) == 1
    first_result = data[0]
    assert first_result["snippet"]["title"] == "Lambda expression"

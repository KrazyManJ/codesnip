from httpx import ASGITransport, AsyncClient
from pydantic_core import ValidationError
import pytest
from app.main import app
from app.model.snippet import Snippet


async_client = AsyncClient(
    transport=ASGITransport(app=app),
    base_url="http://test"
)


@pytest.mark.asyncio
async def test_read_items():
    response = await async_client.get("/snippets")
    assert response.status_code == 200
    response_value = response.json()
    assert type(response_value) == list
    assert len(response_value) == 2
    try:
        Snippet.model_validate(response_value[0])
    except ValidationError:
        pytest.fail("Instance in snippets array is not snippet")

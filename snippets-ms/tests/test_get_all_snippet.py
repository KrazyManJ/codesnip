from pydantic_core import ValidationError
import pytest
from app.model.snippet import Snippet


@pytest.mark.asyncio
async def test_read_items(async_client):
    response = await async_client.get("/snippets")
    assert response.status_code == 200
    response_value = response.json()
    assert type(response_value) == dict
    assert type(response_value["items"]) == list
    assert len(response_value["items"]) == 2
    try:
        Snippet.model_validate(response_value["items"][0])
    except ValidationError:
        pytest.fail("Instance in snippets array is not snippet")

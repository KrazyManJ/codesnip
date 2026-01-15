import pytest
from .conftest import test_snippets

def make_search_result(snippet_obj, highlight_title=""):
    return {
        "snippet": {
            "id": str(snippet_obj.id),
            "title": snippet_obj.title,
            "language": snippet_obj.language,
        },
        "match": {
            "title": highlight_title,
            "description": "",
            "code": ""
        }
    }


@pytest.mark.asyncio
async def test_without_params_success(async_client, mock_search_connector):
    mock_search_connector.search.return_value = [
        make_search_result(test_snippets[0]),
        make_search_result(test_snippets[1])
    ]

    result = await async_client.post("/search")

    assert result.status_code == 200
    data = result.json()
    assert len(data) == 2

    mock_search_connector.search.assert_awaited_once()
    args = mock_search_connector.search.call_args[0]
    assert args[0] == "" or args[0] is None


@pytest.mark.asyncio
async def test_with_query_param_success(async_client, mock_search_connector):
    mock_return = make_search_result(
        test_snippets[1],
        highlight_title="Main <{%HL_START%}>method<{%HL_END%}>"
    )
    mock_search_connector.search.return_value = [mock_return]

    result = await async_client.post("/search?query=method")

    assert result.status_code == 200
    data = result.json()
    assert len(data) == 1
    assert data[0]["match"]["title"] == "Main <{%HL_START%}>method<{%HL_END%}>"

    mock_search_connector.search.assert_awaited_once()
    args, kwargs = mock_search_connector.search.call_args

    if "query" in kwargs:
        assert "method" in kwargs["query"]
    else:
        assert len(args) >= 1
        assert "method" in args[0]


@pytest.mark.asyncio
async def test_with_language_param_success(async_client, mock_search_connector):
    mock_search_connector.search.return_value = [make_search_result(test_snippets[0])]

    result = await async_client.post("/search?lang=python")

    assert result.status_code == 200
    data = result.json()
    assert data[0]["snippet"]["title"] == "Lambda expression"

    mock_search_connector.search.assert_awaited_once()

    args, kwargs = mock_search_connector.search.call_args

    if "language" in kwargs:
        assert kwargs["language"] == "python"
    else:
        assert args[1] == "python"


@pytest.mark.asyncio
async def test_search_empty(async_client, mock_search_connector):
    mock_search_connector.search.return_value = []

    result = await async_client.post("/search?query=NonExisting")

    assert result.status_code == 200
    assert len(result.json()) == 0
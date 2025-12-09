from bson import ObjectId
import pytest_asyncio
from app.repositories.snippet_repository import snippets_collection
from app.model.snippet import Snippet
from app.connectors.grpc_search_connector import search_connector_client
from .utils import meili_utils

test_snippets = [
    Snippet(
        id = ObjectId("6911c38853ed167b0b3cf306"),
        title = "Lambda expression",
        description = "Function as parameter",
        code = "lambda: print('hello_world')",
        language = "Python",
        created_at = "2025-11-10T11:50:48.335000",
        visibility = "public"
    ),
    Snippet(
        id = ObjectId("6911c4059f5ace328a43261b"),
        title = "Main method",
        description = "Method, where code executes",
        code = "class Program {\n\tpublic static void main(String[] args) {\n\t\t\n\t}\n}",
        language = "Java",
        created_at = "2025-11-10T11:52:53.092000",
        visibility = "public"
    )
]


@pytest_asyncio.fixture(autouse=True)
async def before_and_after_each():
    await search_connector_client.start()
    await snippets_collection.delete_many({})
    await meili_utils.clear_meilisearch()
    await snippets_collection.insert_many([s.to_mongo() for s in test_snippets])
    for snippet in test_snippets:
        await search_connector_client.index_snippet(snippet)
    await meili_utils.wait_for_meili_indexing(len(test_snippets))
    yield
    await snippets_collection.delete_many({})
    await meili_utils.clear_meilisearch()
    await search_connector_client.close()
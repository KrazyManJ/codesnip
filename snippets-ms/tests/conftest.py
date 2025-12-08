import asyncio
import os
from bson import ObjectId
import httpx
import pytest_asyncio
from app.services.snippet_service import snippets_collection
from app.services import snippet_controller
from app.model.snippet import Snippet
from app.services.search_service import search_client

test_snippets = [
    Snippet(
        _id = ObjectId("6911c38853ed167b0b3cf306"),
        title = "Lambda expression",
        description = "Function as parameter",
        code = "lambda: print('hello_world')",
        language = "Python",
        created_at = "2025-11-10T11:50:48.335000",
        visibility = "public"
    ),
    Snippet(
        _id = ObjectId("6911c4059f5ace328a43261b"),
        title = "Main method",
        description = "Method, where code executes",
        code = "class Program {\n\tpublic static void main(String[] args) {\n\t\t\n\t}\n}",
        language = "Java",
        created_at = "2025-11-10T11:52:53.092000",
        visibility = "public"
    )
]

from dotenv import load_dotenv

load_dotenv()

MEILI_HOST = os.getenv("MEILI_HOST")
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY")

def get_headers():
    if MEILI_MASTER_KEY:
        return {"Authorization": f"Bearer {MEILI_MASTER_KEY}"}
    return {}

async def clear_meilisearch():
    async with httpx.AsyncClient(timeout=10) as client:
        try:
            await client.delete(
                f"{MEILI_HOST}/indexes/snippets/documents", 
                headers=get_headers()
            )
        except httpx.RequestError as e:
            print(f"Meilisearch cleanup failed: {e}")
            pass
    
async def wait_for_meili_indexing(expected_count: int):
    async with httpx.AsyncClient(timeout=5) as client:
        for _ in range(20):
            try:
                response = await client.get(
                    f"{MEILI_HOST}/indexes/snippets/stats",
                    headers=get_headers()
                )
                if response.status_code == 200:
                    stats = response.json()
                    current_count = stats.get("numberOfDocuments", 0)
                    if current_count == expected_count:
                        return
            except Exception:
                pass
            
            await asyncio.sleep(0.1)
        
        raise RuntimeError(f"Meilisearch failed to index {expected_count} documents in time.")

@pytest_asyncio.fixture(autouse=True)
async def before_and_after_each():
    await search_client.start()
    await snippets_collection.delete_many({})
    await clear_meilisearch()
    await snippets_collection.insert_many([s.model_dump(mode="json") for s in test_snippets])
    for snippet in test_snippets:
        await search_client.index_snippet(snippet)
    await wait_for_meili_indexing(len(test_snippets))
    yield
    await snippets_collection.delete_many({})
    await clear_meilisearch()
    await search_client.close()
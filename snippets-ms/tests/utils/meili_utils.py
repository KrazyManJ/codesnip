import asyncio
import os
from dotenv import load_dotenv
import httpx

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
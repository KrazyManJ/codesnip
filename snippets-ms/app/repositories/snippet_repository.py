import asyncio
import os
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import DeleteResult
from ..model.snippet import UploadSnippet, SnippetDict


MONGO_URL = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URL)
client.get_io_loop = asyncio.get_event_loop
snippets_collection = client["codesnip"]["snippets"]


async def add_snippet(snippet: SnippetDict) -> SnippetDict:
    result = await snippets_collection.insert_one(snippet)
    return await snippets_collection.find_one({"_id": result.inserted_id})


async def get_all_snippets():
    return await snippets_collection.find().to_list()


async def get_snippet_by_id(snippet_id: ObjectId) -> SnippetDict | None:
    return await snippets_collection.find_one({"_id": snippet_id})


async def update_snippet_by_id(snippet_id: ObjectId, snippet_update: UploadSnippet) -> SnippetDict:
    result = await snippets_collection.find_one_and_update(
        {"_id": str(snippet_id)},
        {"$set": snippet_update.model_dump(mode="json")},
        return_document=True
    )
    return result


async def delete_snippet_by_id(snippet_id: ObjectId) -> DeleteResult:
    return await snippets_collection.delete_one({"_id": str(snippet_id)})


async def get_all_languages() -> list[str]:
    return await snippets_collection.distinct("language")
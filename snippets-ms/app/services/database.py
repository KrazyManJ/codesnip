import asyncio
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from ..model.snippet import Snippet, UploadSnippet

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
client.get_io_loop = asyncio.get_event_loop
db = client["codesnip"]
collection = db["snippets"]


async def add_snippet(snippet: Snippet) -> Snippet:
    result = await collection.insert_one(snippet.model_dump())
    return await collection.find_one({"_id": result.inserted_id})


async def get_all_snippets() -> list[Snippet]:
    return await collection.find().to_list()


async def get_snippet_by_id(snippet_id: ObjectId) -> Snippet:
    return await collection.find_one({"_id": snippet_id})


async def update_snippet_by_id(snippet_id: ObjectId, snippet_update: UploadSnippet) -> Snippet:
    return await collection.find_one_and_update(
        {"_id": ObjectId(snippet_id)},
        {"$set": snippet_update.model_dump()},
        return_document=True
    )


async def delete_snippet_by_id(snippet_id: ObjectId):
    return await collection.delete_one({"_id": ObjectId(snippet_id)})

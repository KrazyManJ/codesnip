import asyncio
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from ..model.snippet import Snippet, UploadSnippet

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
client.get_io_loop = asyncio.get_event_loop
db = client["codesnip"]
snippets_collection = db["snippets"]


async def add_snippet(snippet: Snippet):
    result = await snippets_collection.insert_one(snippet.model_dump(mode="json"))
    return await snippets_collection.find_one({"_id": result.inserted_id})


async def get_all_snippets():
    return await snippets_collection.find().to_list()


async def get_snippet_by_id(snippet_id: ObjectId):
    return await snippets_collection.find_one({"_id": snippet_id})


async def update_snippet_by_id(snippet_id: ObjectId, snippet_update: UploadSnippet):
    result = await snippets_collection.find_one_and_update(
        {"_id": str(snippet_id)},
        {"$set": snippet_update.model_dump()},
        return_document=True
    )
    return result


async def delete_snippet_by_id(snippet_id: ObjectId):
    return await snippets_collection.delete_one({"_id": str(snippet_id)})


async def temp_search(query: str = None, language: str = None):

    filters = []

    if query:
        filters.append({
            "$or": [
                {"title": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"code": {"$regex": query, "$options": "i"}}
            ]
        })

    if language:
        filters.append({"language": {"$regex": f'^{language}$', "$options": "i"}})

    if filters:
        query_filter = {"$and": filters} if len(filters) > 1 else filters[0]
    else:
        query_filter = {}

    return await snippets_collection.find(query_filter).to_list()
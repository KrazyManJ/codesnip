from bson import ObjectId
from fastapi_pagination.ext.pymongo import apaginate
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import DeleteResult
from ..model.object_id import PyObjectId

from ..model.snippet import UploadSnippet, SnippetDict


class SnippetRepository:

    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def add_snippet(self, snippet: SnippetDict) -> SnippetDict:
        result = await self.collection.insert_one(snippet)
        return await self.collection.find_one({"_id": result.inserted_id})

    async def get_all_public_snippets(self):
        return await self.collection.find({"visibility": "public"}).to_list()

    async def get_snippet_by_id(self, snippet_id: ObjectId) -> SnippetDict | None:
        result = await self.collection.find_one({"_id": snippet_id})
        
        return result

    async def update_snippet_by_id(self, snippet_id: ObjectId | PyObjectId, snippet_update: UploadSnippet) -> SnippetDict:
        result = await self.collection.find_one_and_update(
            {"_id": snippet_id},
            {"$set": snippet_update.model_dump(mode="json")},
            return_document=True
        )
        return result

    async def delete_snippet_by_id(self, snippet_id: ObjectId) -> DeleteResult:
        return await self.collection.delete_one({"_id": snippet_id})

    async def get_all_public_languages(self) -> list[str]:
        pipeline = [
            {"$match": {"visibility": "public"}},
            {"$group": {"_id": "$language"}},
            {"$sort": {"_id": 1}}
        ]
        cursor = await self.collection.aggregate(pipeline)
        return [doc["_id"] async for doc in cursor]

    async def get_stats(self):
        pipeline = [
            {
                "$match": {"visibility": "public"}
            },
            {
                "$facet": {
                    "lang_stats": [
                        {
                            "$group": {
                                "_id": "$language",
                                "lang": {"$first": "$language"},
                                "snippets_count": {"$sum": 1},
                                "total_bytes": {"$sum": {"$strLenBytes": "$code"}}
                            }
                        },
                        {
                            "$project": {
                                "_id": 0
                            }
                        }
                    ],
                    "total_count": [
                        {
                            "$count": "total_snippets_count"
                        }
                    ],
                    "total_bytes_grand": [
                        {
                            "$group": {
                                "_id": None,
                                "total_bytes": {"$sum": {"$strLenBytes": "$code"}}
                            }
                        }
                    ]
                }
            },
            {
                "$project": {
                    "total_snippets_count": {"$first": "$total_count.total_snippets_count"},
                    "total_bytes": {"$first": "$total_bytes_grand.total_bytes"},
                    "languages_data": "$lang_stats",
                    "_id": 0
                }
            }
        ]
        results = await (await self.collection.aggregate(pipeline)).to_list(length=1)
        return results[0] if results else None

    async def get_all_user_snippets(self, user_id: str):
        return await self.collection.find({"author.id": user_id}).to_list()

    async def get_paginated_snippets_by_query(self, query: dict):
        return await apaginate(self.collection, query)

    async def get_snippets_in_batch(self, snippet_ids: list[str], user_id: str):
        return await self.collection.find({
            "_id": {"$in": snippet_ids},
            "$or": [
                {"visibility": "public"},
                {
                    "visibility": "private",
                    "author.id": user_id
                }
            ]
        }).to_list()

from fastapi_pagination.ext.pymongo import apaginate
from pymongo.asynchronous.collection import AsyncCollection

from app.model.save import Save


class SaveRepository:

    def __init__(self, collection: AsyncCollection):
        self.collection = collection
        
    async def save(self, save: Save, user_id: str):
        result = await self.collection.insert_one({
            "user_id": user_id,
            "snippet_id": save.snippet_id,
            "saved_at": save.saved_at,
        })
        return await self.collection.find_one({"_id": result.inserted_id})

    async def unsave(self, snippet_id, user_id):
        return await self.collection.delete_one({
            "snippet_id": snippet_id,
            "user_id": user_id,
        })

    async def get_save(self, snippet_id, user_id):
        return await self.collection.find_one({
            "snippet_id": snippet_id,
            "user_id": user_id,
        })

    async def get_all_saves_paginated(self, query: dict):
        return await apaginate(self.collection, query)

    async def get_ids_of_saved_snippets_for_user(self, user_id, snippet_ids: list[str]):
        return await self.collection.find({
            "user_id": user_id,
            "snippet_id": {"$in": snippet_ids},
        }).to_list()
    
    async def get_snippet_stats(self, snippet_id):
        pipeline = [
            {
                "$match": {"snippet_id": snippet_id}
            },
            {
                "$group": {
                    "_id": "$snippet_id",
                    "save_count": {"$sum": 1}
                }
            }
        ]
        results = await (await self.collection.aggregate(pipeline)).to_list()
        print(results)
        return results[0] if results else {"save_count": 0}

from datetime import datetime

from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection

from app.model.save import Save


class SaveRepository:
    
    def __init__(self, collection: AsyncCollection):
        self.collection = collection
        
    async def save(self, save: Save, user_id: str):
        result = await self.collection.insert_one({
            "user_id": user_id,
            "snippet_id": save.snippet_id,
            "created_at": save.created_at,
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
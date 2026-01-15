from fastapi import HTTPException, status
from fastapi_pagination import Page
from fastapi_pagination.ext.pymongo import apaginate

from app.model.save import UploadSave, Save, SaveStatusRequestBody
from app.model.user import User
from app.repositories.save_repository import SaveRepository


class SaveService:
    
    def __init__(self, repository: SaveRepository):
        self.repository = repository

    async def save_snippet(self, user: User, body: UploadSave):
        is_already_saved = (await self.repository.get_save(body.snippet_id, user.id)) is not None
        
        if is_already_saved:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"This snippet is already saved.",
            )
        
        return await self.repository.save(
            save=Save(
                snippet_id=body.snippet_id,
            ),
            user_id=user.id,
        )

    async def unsave_snippet(self, user: User, snippet_id: str):
        save_in_db = await self.repository.get_save(snippet_id, user.id)

        if save_in_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"This snippet is not saved.",
            )
        
        await self.repository.unsave(
            snippet_id=snippet_id,
            user_id=user.id,
        )
    
    async def get_all_saves_of_user(self, user_id) -> Page[Save]:
        return await self.repository.get_all_saves_paginated({"user_id": user_id})

    async def get_snippet(self, user, snippet_id):
        return await self.repository.get_save(snippet_id, user.id)

    async def check_status_of_snippets_for_user(self, user, save_status_request: SaveStatusRequestBody):
        return await self.repository.get_ids_of_saved_snippets_for_user(
            user.id, 
            save_status_request.snippet_ids
        )
        
    async def get_status_of_snippet(self, snippet_id):
        return await self.repository.get_snippet_stats(snippet_id) 
        
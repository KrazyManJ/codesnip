from bson import ObjectId
from fastapi import HTTPException, status

from app.model.save import UploadSave, Save
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
        if not ObjectId.is_valid(snippet_id):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=f"Invalid snippet ID: {snippet_id}",
            )
        
        is_present = (await self.repository.get_save(snippet_id, user.id)) is not None

        if not is_present:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"This snippet is already saved.",
            )
        
        await self.repository.unsave(
            snippet_id=snippet_id,
            user_id=user.id,
        )
        
from bson import ObjectId
from fastapi import HTTPException
from .model.snippet import Snippet
from .services import database


async def validate_snippet_id(snippet_id: str) -> Snippet:
    if not ObjectId.is_valid(snippet_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid format of snippet id"
        )
    snippet = await database.get_snippet_by_id(snippet_id)
    if snippet is None:
        raise HTTPException(
            status_code=404,
            detail=f"Snippet with id '{snippet_id}' not found"
        )
    return Snippet(**snippet)

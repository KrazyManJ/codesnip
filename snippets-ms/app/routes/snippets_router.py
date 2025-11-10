
from fastapi import APIRouter, Depends
from typing import Annotated

from ..model.snippet import Snippet, UploadSnippet
from ..services import database
from ..dependencies import validate_snippet_id


router = APIRouter(prefix="/snippets")


@router.post("", status_code=201)
async def upload_snippet(snippet: UploadSnippet) -> Snippet:
    return await database.add_snippet(snippet)


@router.get("")
async def all_snippets() -> list[Snippet]:
    return await database.get_all_snippets()


@router.get("/{snippet_id}")
async def get_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> Snippet:
    return snippet


@router.put("/{snippet_id}")
async def update_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)], snippet_update: UploadSnippet) -> Snippet:
    return await database.update_snippet_by_id(snippet.id, snippet_update)


@router.delete("/{snippet_id}", status_code=204)
async def delete_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> None:
    await database.delete_snippet_by_id(snippet.id)


@router.post("/search")
async def search(query: str) -> list[Snippet]:
    return await database.temp_search(query)
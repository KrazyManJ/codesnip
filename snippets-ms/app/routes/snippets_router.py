
from fastapi import APIRouter, Depends
from typing import Annotated

from ..model.snippet import Snippet, UploadSnippet
from ..services import snippet_service
from ..services.search_service import search_client
from ..dependencies import validate_snippet_id


router = APIRouter(prefix="/snippets", tags=["Snippets"])


@router.post("", status_code=201)
async def upload_snippet(snippet: UploadSnippet) -> Snippet:
    newSnippet = await snippet_service.add_snippet(snippet)
    await search_client.index_snippet(newSnippet)
    return newSnippet


@router.get("")
async def all_snippets() -> list[Snippet]:
    return await snippet_service.get_all_snippets()


@router.get("/{snippet_id}")
async def get_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> Snippet:
    return snippet


@router.put("/{snippet_id}")
async def update_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)], snippet_update: UploadSnippet) -> Snippet:
    updatedSnippet = await snippet_service.update_snippet_by_id(snippet.id, snippet_update)
    search_client.index_snippet(updatedSnippet)
    return updatedSnippet


@router.delete("/{snippet_id}", status_code=204)
async def delete_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> None:
    # TODO: Delete index from Meilisearchs
    await snippet_service.delete_snippet_by_id(snippet.id)
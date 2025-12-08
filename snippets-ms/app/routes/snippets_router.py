
from fastapi import APIRouter, BackgroundTasks, Depends
from typing import Annotated

from ..model.snippet import Snippet, UploadSnippet
from ..services import snippet_service
from ..services.search_service import search_client
from ..dependencies import validate_snippet_id


router = APIRouter(prefix="/snippets", tags=["Snippets"])


@router.post("", status_code=201)
async def upload_snippet(snippet: UploadSnippet, background_tasks: BackgroundTasks) -> Snippet:
    new_snippet = await snippet_service.add_snippet(snippet)
    background_tasks.add_task(search_client.index_snippet, Snippet(**new_snippet))
    return new_snippet


@router.get("")
async def all_snippets() -> list[Snippet]:
    return await snippet_service.get_all_snippets()


@router.get("/{snippet_id}")
async def get_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> Snippet:
    return snippet


@router.put("/{snippet_id}")
async def update_snippet(
    snippet: Annotated[Snippet, Depends(validate_snippet_id)], 
    snippet_update: UploadSnippet,
    background_tasks: BackgroundTasks
) -> Snippet:
    updated_snippet = await snippet_service.update_snippet_by_id(snippet.id, snippet_update)
    background_tasks.add_task(search_client.index_snippet, Snippet(**updated_snippet))
    return updated_snippet


@router.delete("/{snippet_id}", status_code=204)
async def delete_snippet(
    snippet: Annotated[Snippet, Depends(validate_snippet_id)],
    background_tasks: BackgroundTasks
) -> None:
    await snippet_service.delete_snippet_by_id(snippet.id)
    background_tasks.add_task(search_client.delete_snippet, str(snippet.id))
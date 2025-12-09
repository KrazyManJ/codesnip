
from fastapi import APIRouter, BackgroundTasks, Depends, Query
from typing import Annotated

from ..model.snippet import Snippet, UploadSnippet
from ..model.search import SearchResult
from ..services import snippet_service
from ..services.search_service import search_client
from ..dependencies import validate_snippet_id


router = APIRouter(tags=["Snippets"])


snippets_router = APIRouter(prefix="/snippets")


@snippets_router.post("", status_code=201)
async def upload_snippet(snippet: UploadSnippet, background_tasks: BackgroundTasks) -> Snippet:
    return await snippet_service.add_snippet(snippet, background_tasks)


@snippets_router.get("")
async def all_snippets() -> list[Snippet]:
    return await snippet_service.get_all_snippets()


@snippets_router.get("/{snippet_id}")
async def get_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> Snippet:
    return snippet


@snippets_router.put("/{snippet_id}")
async def update_snippet(
    snippet: Annotated[Snippet, Depends(validate_snippet_id)],
    snippet_update: UploadSnippet,
    background_tasks: BackgroundTasks
) -> Snippet:
    return await snippet_service.update_snippet_by_id(snippet.id, snippet_update, background_tasks)


@snippets_router.delete("/{snippet_id}", status_code=204)
async def delete_snippet(
    snippet: Annotated[Snippet, Depends(validate_snippet_id)],
    background_tasks: BackgroundTasks
) -> None:
    return await snippet_service.delete_snippet_by_id(snippet.id, background_tasks)


@router.post("/search")
async def search(
    query: str = None,
    language: str = Query(default=None, alias="lang")
) -> list[SearchResult]:
    return await search_client.search(query, language)


@router.get("/langs")
async def get_all_languages() -> list[str]:
    return await snippet_service.get_all_languages()


router.include_router(snippets_router)

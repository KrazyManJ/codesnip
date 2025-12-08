
from bson import ObjectId
from fastapi import BackgroundTasks
from .search_service import search_client
from . import snippet_service
from ..model.snippet import UploadSnippet, SnippetDict, Snippet


async def add_snippet(
    snippet: UploadSnippet,
    background_tasks: BackgroundTasks = None
) -> SnippetDict:
    result_snippet = await snippet_service.add_snippet(snippet.model_dump(mode="json"))
    if background_tasks:
        background_tasks.add_task(search_client.index_snippet, Snippet(**result_snippet))
    else:
        await search_client.index_snippet(Snippet(**result_snippet))
    return result_snippet


async def update_snippet_by_id(
    snippet_id: ObjectId,
    snippet_update: UploadSnippet,
    background_tasks: BackgroundTasks = None
) -> SnippetDict:
    updated_snippet = await snippet_service.update_snippet_by_id(snippet_id, snippet_update)
    print(updated_snippet)
    if background_tasks:
        background_tasks.add_task(search_client.index_snippet, Snippet(**updated_snippet))
    else:
        await search_client.index_snippet(Snippet(**updated_snippet))
    return updated_snippet


async def delete_snippet_by_id(
    snippet_id: ObjectId,
    background_tasks: BackgroundTasks = None
):
    await snippet_service.delete_snippet_by_id(snippet_id)
    if background_tasks:
        background_tasks.add_task(search_client.delete_snippet, str(snippet_id))
    else:
        await search_client.delete_snippet(str(snippet_id))
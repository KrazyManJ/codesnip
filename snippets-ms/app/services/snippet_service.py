from bson import ObjectId
from fastapi import BackgroundTasks
from ..connectors.grpc_search_connector import search_connector_client
from ..repositories import snippet_repository
from ..model.snippet import UploadSnippet, SnippetDict, Snippet
from ..model.search import SearchResultDict
from ..model.object_id import PyObjectId


async def add_snippet(
    snippet: Snippet,
    background_tasks: BackgroundTasks = None
) -> Snippet:
    result_snippet_dict = await snippet_repository.add_snippet(snippet.model_dump(mode="json"))
    result_snippet = Snippet(**result_snippet_dict)
    if background_tasks:
        background_tasks.add_task(search_connector_client.index_snippet, result_snippet)
    else:
        await search_connector_client.index_snippet(result_snippet)
    return result_snippet


async def get_all_snippets() -> list[SnippetDict]:
    return await snippet_repository.get_all_snippets()


async def get_snippet_by_id(snippet_id: str) -> SnippetDict:
    return await snippet_repository.get_snippet_by_id(ObjectId(snippet_id))


async def update_snippet_by_id(
    snippet_id: ObjectId | PyObjectId,
    snippet_update: UploadSnippet,
    background_tasks: BackgroundTasks = None
) -> SnippetDict:
    updated_snippet = await snippet_repository.update_snippet_by_id(snippet_id, snippet_update)
    if background_tasks:
        background_tasks.add_task(search_connector_client.index_snippet, Snippet(**updated_snippet))
    else:
        await search_connector_client.index_snippet(Snippet(**updated_snippet))
    return updated_snippet


async def delete_snippet_by_id(
    snippet_id: ObjectId | PyObjectId,
    background_tasks: BackgroundTasks = None
) -> None:
    delete_result = await snippet_repository.delete_snippet_by_id(snippet_id)
    if delete_result.deleted_count == 0:
        return
    
    if background_tasks:
        background_tasks.add_task(search_connector_client.delete_snippet, str(snippet_id))
    else:
        await search_connector_client.delete_snippet(str(snippet_id))


async def search(query: str, language: str = None) -> SearchResultDict:
    return await search_connector_client.search(query, language)


async def get_all_languages() -> list[str]:
    return await snippet_repository.get_all_languages()


async def get_stats():
    return await snippet_repository.get_stats()
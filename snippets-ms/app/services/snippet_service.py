from bson import ObjectId
from fastapi import BackgroundTasks
from ..connectors.grpc_search_connector import GRPCSearchConnector
from ..repositories.snippet_repository import SnippetRepository
from ..model.snippet import UploadSnippet, SnippetDict, Snippet
from ..model.search import SearchResultDict
from ..model.object_id import PyObjectId

class SnippetService:
    
    def __init__(
        self, 
        repository: SnippetRepository, 
        search_connector_client: GRPCSearchConnector,
        background_tasks: BackgroundTasks
    ):
        self.snippet_repository = repository
        self.search_connector_client = search_connector_client
        self.background_tasks = background_tasks

    async def add_snippet(
        self,
        snippet: Snippet
    ) -> Snippet:
        result_snippet_dict = await self.snippet_repository.add_snippet(snippet.model_dump(mode="json"))
        result_snippet = Snippet(**result_snippet_dict)
        if self.background_tasks:
            self.background_tasks.add_task(self.search_connector_client.index_snippet, result_snippet)
        else:
            await self.search_connector_client.index_snippet(result_snippet)
        return result_snippet
    
    
    async def get_all_snippets(self) -> list[SnippetDict]:
        return await self.snippet_repository.get_all_public_snippets()
    
    
    async def get_snippet_by_id(self, snippet_id: str) -> SnippetDict:
        return await self.snippet_repository.get_snippet_by_id(ObjectId(snippet_id))
    
    
    async def update_snippet_by_id(self,
        snippet_id: ObjectId | PyObjectId,
        snippet_update: UploadSnippet
    ) -> SnippetDict:
        updated_snippet = await self.snippet_repository.update_snippet_by_id(snippet_id, snippet_update)
        if self.background_tasks:
            self.background_tasks.add_task(self.search_connector_client.index_snippet, Snippet(**updated_snippet))
        else:
            await self.search_connector_client.index_snippet(Snippet(**updated_snippet))
        return updated_snippet
    
    
    async def delete_snippet_by_id(self,
        snippet_id: ObjectId | PyObjectId
    ) -> None:
        delete_result = await self.snippet_repository.delete_snippet_by_id(snippet_id)
        if delete_result.deleted_count == 0:
            return
        
        if self.background_tasks:
            self.background_tasks.add_task(self.search_connector_client.delete_snippet, str(snippet_id))
        else:
            await self.search_connector_client.delete_snippet(str(snippet_id))
    
    
    async def search(self, query: str, language: str = None) -> SearchResultDict:
        return await self.search_connector_client.search(query, language)
    
    
    async def get_all_languages(self,) -> list[str]:
        return await self.snippet_repository.get_all_languages()
    
    
    async def get_stats(self,):
        return await self.snippet_repository.get_stats()
    
    
    async def get_all_user_snippets(self, user_id: str):
        return await self.snippet_repository.get_all_user_snippets(user_id)
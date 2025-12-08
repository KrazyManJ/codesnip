import os
import grpc
import logging
import search_pb2_grpc, search_pb2

SEARCH_SERVICE_ADDRESS = os.getenv("SEARCH_SERVICE_ADDRESS", "localhost:50051")

logger = logging.getLogger(__name__)

class SearchClient:
    def __init__(self):
        self.channel = None
        self.stub = None

    async def start(self):
        logger.info(f"Connecting to Search Service at {SEARCH_SERVICE_ADDRESS}")
        self.channel = grpc.aio.insecure_channel(SEARCH_SERVICE_ADDRESS)
        self.stub = search_pb2_grpc.SearchServiceStub(self.channel)

    async def close(self):
        if self.channel:
            await self.channel.close()
            logger.info("Search Service channel closed")

    async def index_snippet(self, snippet_data):
        if not self.stub:
            logger.error("gRPC Client is not initialized!")
            return
            
        try:
            request = search_pb2.SnippetDocument(
                id=str(snippet_data.id),
                title=snippet_data.title,
                description=snippet_data.description,
                code=snippet_data.code,
                language=snippet_data.language
            )
            response = await self.stub.IndexSnippet(request)
            if response.success:
                logger.info(f"Snippet {snippet_data.id} was successfully indexed.")
            else:
                logger.warning(f"Search Service refused to index snippet {snippet_data.id}.")
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e}")

    async def search(self, query: str, language: str = None):
        if not self.stub:
            logger.error("gRPC Client is not initialized!")
            return []

        try:
            request = search_pb2.SearchRequest(
                query=query,
                language_filter=language if language else "",
                limit=20
            )
            response = await self.stub.Search(request)
            
            results = []
            for res in response.results:
                results.append({
                    "id": res.id,
                    "title": res.title,
                    "language": res.language,
                    "match_preview": res.formatted_match
                })
            return results

        except grpc.RpcError as e:
            logger.error(f"gRPC error: {e}")
            return []
        
    async def delete_snippet(self, snippet_id: str):
        if not self.stub:
            logger.error("gRPC Client not initialized")
            return

        try:
            request = search_pb2.DeleteSnippetRequest(id=snippet_id)
            response = await self.stub.DeleteSnippet(request)
            
            if response.success:
                logger.info(f"Snippet {snippet_id} deleted from index.")
            else:
                logger.warning(f"Failed to delete snippet {snippet_id} from index.")
                
        except grpc.RpcError as e:
            logger.error(f"gRPC error during delete: {e}")

search_client = SearchClient()
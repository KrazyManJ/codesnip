import os
import time
import logging
from concurrent import futures

import grpc
import meilisearch

import search_pb2
import search_pb2_grpc

MEILI_HOST = os.getenv("MEILI_HOST", "http://localhost:7700")
MEILI_MASTER_KEY = os.getenv("MEILI_MASTER_KEY")
GRPC_PORT = os.getenv("GRPC_PORT", "50051")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SearchService(search_pb2_grpc.SearchServiceServicer):
    def __init__(self):
        self.client = meilisearch.Client(MEILI_HOST, MEILI_MASTER_KEY)
        self.index_name = "snippets"
        self._setup_index()

    def _setup_index(self):
        try:
            self.client.create_index(self.index_name, {'primaryKey': 'id'})
            index = self.client.index(self.index_name)
            
            index.update_filterable_attributes(['language'])
            
            index.update_searchable_attributes(['title', 'description', 'code', 'language'])
            
            logger.info(f"Meilisearch index '{self.index_name}' configured.")
        except Exception as e:
            logger.error(f"Error configuring Meilisearch: {e}")

    def IndexSnippet(self, request, context):
        try:
            document = {
                "id": request.id,
                "title": request.title,
                "description": request.description,
                "code": request.code,
                "language": request.language
            }
            self.client.index(self.index_name).add_documents([document])
            logger.info(f"Indexed snippet: {request.id}")
            return search_pb2.IndexResponse(success=True)
        except Exception as e:
            logger.error(f"Failed to index snippet {request.id}: {e}")
            return search_pb2.IndexResponse(success=False)

    def Search(self, request, context):
        try:
            filter_query = None
            if request.language_filter:
                filter_query = f"language = '{request.language_filter}'"

            search_params = {
                'limit': request.limit if request.limit > 0 else 20,
                'attributesToHighlight': ['title', 'description', 'code'],
                'highlightPreTag': '<b>',
                'highlightPostTag': '</b>'
            }
            
            if filter_query:
                search_params['filter'] = filter_query

            results = self.client.index(self.index_name).search(request.query, search_params)
            
            grpc_results = []
            for hit in results['hits']:
                formatted = hit.get('_formatted', hit)
                
                match_preview = ""
                if '<b>' in formatted.get('code', ''):
                    match_preview = f"Code: ...{formatted['code'][:150]}..."
                elif '<b>' in formatted.get('description', ''):
                    match_preview = formatted['description']
                else:
                    match_preview = formatted.get('description', '')

                grpc_results.append(search_pb2.SearchResult(
                    id=hit['id'],
                    title=formatted['title'],
                    language=hit['language'],
                    formatted_match=match_preview
                ))

            return search_pb2.SearchResponse(results=grpc_results)

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return search_pb2.SearchResponse(results=[])
        
    def DeleteSnippet(self, request, context):
        try:
            self.client.index(self.index_name).delete_document(request.id)
            logger.info(f"Deleted snippet from index: {request.id}")
            return search_pb2.DeleteResponse(success=True)
        except Exception as e:
            logger.error(f"Failed to delete snippet {request.id}: {e}")
            return search_pb2.DeleteResponse(success=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    search_pb2_grpc.add_SearchServiceServicer_to_server(SearchService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    logger.info(f"Search Service running on port {GRPC_PORT}...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
from bson import ObjectId
from app.services.snippet_service import add_snippet, snippets_collection
from app.services.search_service import search_client
from app.model.snippet import Snippet

async def seed_data():
    count = await snippets_collection.count_documents({})
    
    if (count > 0):
        return
    
    snippets = [
        Snippet(
            _id = str(ObjectId()),
            title = "Lambda expression",
            description = "Function as parameter",
            code = "lambda: print('hello_world')",
            language = "python",
            created_at = "2025-11-10T11:50:48.335000",
            visibility = "public"
        ),
        Snippet(
            _id = str(ObjectId()),
            title = "Main function",
            description = "Main",
            code = "public static void main(String[] args)",
            language = "java",
            created_at = "2025-11-10T11:50:48.335000",
            visibility = "public"
        )
    ]
    
    
    for snippet in snippets:
        await search_client.index_snippet(snippet)
        await add_snippet(snippet)
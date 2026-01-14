from bson import ObjectId
from app.services import snippet_service
from app.model.snippet import Snippet

async def seed_data_if_empty():
    count = len(await snippet_service.get_all_snippets())
    
    if count > 0:
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
        await snippet_service.add_snippet(snippet)
        
    print("Data initialized!")
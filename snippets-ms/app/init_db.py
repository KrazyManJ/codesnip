from bson import ObjectId
from app.services.snippet_service import snippets_collection


async def seed_data():
    count = await snippets_collection.count_documents({})
    
    if (count > 0):
        return
    
    print("Initializing data...")
    
    await snippets_collection.insert_many([
        {
            "_id": str(ObjectId()),
            "title": "Lambda expression",
            "description": "Function as parameter",
            "code": "lambda: print('hello_world')",
            "language": "python",
            "created_at": "2025-11-10T11:50:48.335000",
            "visibility": "public"
        },
        {
            "_id": str(ObjectId()),
            "title": "Function definition",
            "description": "Function",
            "code": "func functionName()",
            "language": "swift",
            "created_at": "2025-11-10T11:50:48.335000",
            "visibility": "public"
        },
        {
            "_id": str(ObjectId()),
            "title": "Main method",
            "description": "Method, where code executes",
            "code": "class Program {\n\tpublic static void main(String[] args) {\n\t\t\n\t}\n}",
            "language": "java",
            "created_at": "2025-11-10T11:52:53.092000",
            "visibility": "public"
        }
    ])
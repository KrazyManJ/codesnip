import pytest_asyncio
from app.services.database import snippets_collection

@pytest_asyncio.fixture(autouse=True)
async def before_and_after_each():
    await snippets_collection.delete_many({})
    await snippets_collection.insert_many([
        {
            "_id": "6911c38853ed167b0b3cf306",
            "title": "Lambda expression",
            "description": "Function as parameter",
            "code": "lambda: print('hello_world')",
            "language": "Python",
            "created_at": "2025-11-10T11:50:48.335000",
            "visibility": "public"
        },
        {
            "_id": "6911c4059f5ace328a43261b",
            "title": "Main method",
            "description": "Method, where code executes",
            "code": "class Program {\n\tpublic static void main(String[] args) {\n\t\t\n\t}\n}",
            "language": "Java",
            "created_at": "2025-11-10T11:52:53.092000",
            "visibility": "public"
        }
    ])
    yield
    await snippets_collection.delete_many({})
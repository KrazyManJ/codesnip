import warnings
from datetime import datetime

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock

from httpx import AsyncClient, ASGITransport
from testcontainers.mongodb import MongoDbContainer
from pymongo import AsyncMongoClient
from app.main import app
from app.dependencies import get_database, get_search_connector, get_current_user_allow_none
from app.connectors.grpc_search_connector import GRPCSearchConnector
from app.model.object_id import PyObjectId
from app.model.snippet import User, Snippet, Visibility

warnings.filterwarnings("ignore", category=DeprecationWarning, module="testcontainers")

TEST_USER = User(
    id="test-user-id-123",
    username="testuser",
    email_hash="hash-of-test-email"
)
TEST_INVALID_USER = User(
    id="test-invalid-user-id-123",
    username="testinvaliduser",
    email_hash="hash-of-test-invalidemail"
)

test_snippets = [
    Snippet(
        id = PyObjectId("6911c38853ed167b0b3cf306"),
        title = "Lambda expression",
        description = "Function as parameter",
        code = "lambda: print('hello_world')",
        language = "Python",
        created_at = datetime.fromisoformat("2025-11-10T11:50:48.335000"),
        visibility = Visibility.PUBLIC,
        author = TEST_USER,
    ),
    Snippet(
        id = PyObjectId("6911c4059f5ace328a43261b"),
        title = "Main method",
        description = "Method, where code executes",
        code = "class Program {\n\tpublic static void main(String[] args) {\n\t\t\n\t}\n}",
        language = "Java",
        created_at = datetime.fromisoformat("2025-11-10T11:50:48.335000"),
        visibility = Visibility.PUBLIC,
        author = TEST_INVALID_USER,
    ),
    Snippet(
        id = PyObjectId("696843588e0bf4375c065efd"),
        title = "Declaration",
        description = "Declaration of pointer of pointer of int. This is private one!",
        code = "int** ptr;",
        language = "C++",
        created_at = datetime.fromisoformat("2025-11-10T11:50:48.335000"),
        visibility = Visibility.PRIVATE,
        author = TEST_INVALID_USER,
    )
]


@pytest.fixture(scope="session")
def mongo_container():
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo


@pytest_asyncio.fixture
async def db_client(mongo_container):
    mongo_url = mongo_container.get_connection_url()
    mongo_client = AsyncMongoClient(mongo_url)
    await mongo_client["codesnip"]["snippets"].insert_many([s.to_mongo() for s in test_snippets])

    try:
        yield mongo_client
    finally:
        await mongo_client["codesnip"]["snippets"].delete_many({})
        await mongo_client.close()
        


@pytest.fixture
def mock_search_connector():
    mock = AsyncMock(spec=GRPCSearchConnector)

    mock.search.return_value = []
    mock.index_snippet.return_value = None
    mock.delete_snippet.return_value = None

    return mock


@pytest_asyncio.fixture(autouse=True)
async def setup_overrides(db_client, mock_search_connector):
    async def override_get_database():
        yield db_client

    async def override_get_search_connector():
        yield mock_search_connector

    def override_get_current_user():
        return TEST_USER

    app.dependency_overrides[get_database] = override_get_database
    app.dependency_overrides[get_search_connector] = override_get_search_connector
    app.dependency_overrides[get_current_user_allow_none] = override_get_current_user

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def unauthenticated():
    app.dependency_overrides[get_current_user_allow_none] = lambda: None


@pytest_asyncio.fixture
async def async_client(setup_overrides):
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac

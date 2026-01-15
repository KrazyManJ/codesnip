from datetime import datetime

import pytest
import pytest_asyncio
from bson import ObjectId
from httpx import AsyncClient, ASGITransport
from pymongo import AsyncMongoClient
from testcontainers.mongodb import MongoDbContainer

from app.model.save import Save
from app.model.user import User
from app.main import app
from app.dependencies import get_database, get_current_user_allow_none

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

def _create_save(user: User):
    return {
        "user_id": user.id,
        "snippet_id": str(ObjectId()),
        "saved_at": datetime.now().isoformat(),
    }

TEST_SAVES = [
    _create_save(TEST_USER),
    _create_save(TEST_USER),
    _create_save(TEST_INVALID_USER),
    _create_save(TEST_INVALID_USER),
]

@pytest.fixture(scope="session")
def mongo_container():
    with MongoDbContainer("mongo:latest") as mongo:
        yield mongo


@pytest_asyncio.fixture
async def db_client(mongo_container):
    mongo_url = mongo_container.get_connection_url()
    mongo_client = AsyncMongoClient(mongo_url)
    await mongo_client["codesnip"]["saves"].insert_many([s for s in TEST_SAVES])

    try:
        yield mongo_client
    finally:
        await mongo_client["codesnip"]["saves"].delete_many({})
        await mongo_client.close()
        
        
@pytest_asyncio.fixture(autouse=True)
async def setup_overrides(db_client):
    async def override_get_database():
        yield db_client

    def override_get_current_user():
        return TEST_USER

    app.dependency_overrides[get_database] = override_get_database
    app.dependency_overrides[get_current_user_allow_none] = override_get_current_user

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def unauthenticated():
    app.dependency_overrides[get_current_user_allow_none] = lambda: None


@pytest.fixture
def authenticated_as_invalid():
    def override_get_current_user():
        return TEST_INVALID_USER
    app.dependency_overrides[get_current_user_allow_none] = override_get_current_user


@pytest_asyncio.fixture
async def async_client(setup_overrides):
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as ac:
        yield ac

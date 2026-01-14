from bson import ObjectId
from fastapi import HTTPException, Depends, BackgroundTasks
from pymongo.asynchronous.collection import AsyncCollection

from .model.snippet import Snippet
from .services.snippet_service import SnippetService
from .repositories.snippet_repository import SnippetRepository
from .connectors.grpc_search_connector import GRPCSearchConnector

import os
from typing import Annotated, Any, AsyncGenerator, Mapping
from pymongo import AsyncMongoClient
from dotenv import load_dotenv


async def get_database() -> AsyncGenerator[AsyncMongoClient[Mapping[str, Any] | Any], Any]:
    load_dotenv()

    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_USER = os.environ.get("MONGO_USER")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:27017/admin?authSource=admin"

    client = AsyncMongoClient(MONGO_URL)
    try:
        yield client
    finally:
        await client.close()


def get_snippets_collection(client: Annotated[AsyncMongoClient, Depends(get_database)]) -> AsyncCollection:
    return client["codesnip"]["snippets"]


def get_snippet_repository(
    collection: Annotated[AsyncCollection, Depends(get_snippets_collection)]) -> SnippetRepository:
    return SnippetRepository(collection)


async def get_search_connector():
    connector = GRPCSearchConnector()
    try:
        yield connector
    finally:
        await connector.close()


def get_snippet_service(
    repository: Annotated[SnippetRepository, Depends(get_snippet_repository)],
    search_connector: Annotated[GRPCSearchConnector, Depends(get_search_connector)],
    background_tasks: BackgroundTasks
) -> SnippetService:
    return SnippetService(
        repository=repository,
        search_connector_client=search_connector,
        background_tasks=background_tasks
    )


async def validate_snippet_id(
    snippet_id: str,
    snippet_service: Annotated[SnippetService, Depends(get_snippet_service)]
) -> Snippet:
    if not ObjectId.is_valid(snippet_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid format of snippet id"
        )
    snippet = await snippet_service.get_snippet_by_id(snippet_id)
    if snippet is None:
        raise HTTPException(
            status_code=404,
            detail=f"Snippet with id '{snippet_id}' not found"
        )
    return Snippet(**snippet)

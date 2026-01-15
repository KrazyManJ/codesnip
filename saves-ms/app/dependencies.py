import hashlib

from bson import ObjectId
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pymongo.asynchronous.collection import AsyncCollection

from app.model.user import User
from app.repositories.save_repository import SaveRepository
from app.services.auth import AuthHandler

import os
from typing import Annotated, Any, AsyncGenerator, Mapping
from pymongo import AsyncMongoClient
from dotenv import load_dotenv

from app.services.save_service import SaveService

security = HTTPBearer()


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


def get_saves_collection(client: Annotated[AsyncMongoClient, Depends(get_database)]) -> AsyncCollection:
    return client["codesnip"]["saves"]


def get_save_repository(
    collection: Annotated[AsyncCollection, Depends(get_saves_collection)]) -> SaveRepository:
    return SaveRepository(collection)


def get_save_service(
    repository: Annotated[SaveRepository, Depends(get_save_repository)]
) -> SaveService:
    return SaveService(
        repository=repository
    )


def get_auth_handler() -> AuthHandler:
    return AuthHandler()


async def get_current_user_allow_none(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    auth_handler: Annotated[AuthHandler, Depends(get_auth_handler)]
) -> User | None:
    token = credentials.credentials
    payload = auth_handler.verify_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        return None

    email_bytes = payload.get("email").strip().lower().encode('utf-8')

    return User(
        id=user_id,
        username=payload.get("preferred_username"),
        email_hash=hashlib.md5(email_bytes).hexdigest(),
    )


async def get_current_user(user: Annotated[User | None, Depends(get_current_user_allow_none)]) -> User:
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Token missing user ID"
        )
    return user


def verify_object_id(snippet_id: str):
    if not ObjectId.is_valid(snippet_id):
        raise HTTPException(
            status_code=422,
            detail=f"ID '{snippet_id}' is not valid id"
        )
    return snippet_id
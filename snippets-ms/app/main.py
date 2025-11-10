import asyncio
from datetime import datetime
from enum import Enum
from typing import Annotated, Optional
from fastapi import Depends, FastAPI, HTTPException
from fastapi.concurrency import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict, field_serializer
from bson import ObjectId
import asyncio

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
client.get_io_loop = asyncio.get_event_loop
db = client["codesnip"]
collection = db["snippets"]

app = FastAPI()

class PyObjectId(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        from pydantic_core import core_schema
        return core_schema.union_schema([
            core_schema.is_instance_schema(ObjectId),
            core_schema.chain_schema([
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(cls.validate),
            ])
        ])

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}

class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"

class UploadSnippet(BaseModel):
    title: str
    description: str
    code: str
    language: str
    created_at: datetime
    visibility: Visibility = Visibility.PUBLIC

class ObjectIdBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name = True
    )

    @field_serializer('id')
    def serialize_object_id(self, value: Optional[PyObjectId], _info):
        if value is not None:
            return str(value)
        return value

class Snippet(UploadSnippet, ObjectIdBaseModel):
    pass


@app.get("/")
def status():
    return { "status": "OK" }


@app.post("/snippets")
async def upload_snippet(snippet: UploadSnippet) -> Snippet:
    result = await collection.insert_one(snippet.model_dump())
    return await collection.find_one({"_id": result.inserted_id})


@app.get("/snippets")
async def all_snippets() -> list[Snippet]:
    return await collection.find().to_list()


async def validate_snippet_id(snippet_id: str) -> Snippet:
    if not ObjectId.is_valid(snippet_id):
        raise HTTPException(
            status_code = 400,
            detail = "Invalid format of snippet id"
        )
    snippet = await collection.find_one({"_id": ObjectId(snippet_id)})
    if snippet is None:
        raise HTTPException(
            status_code=404,
            detail=f"Snippet with id '{snippet_id}' not found"
        )
    return snippet


@app.get("/snippets/{snippet_id}")
async def get_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> Snippet:
    return snippet


@app.put("/snippets/{snippet_id}")
async def update_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)], snippet_update: UploadSnippet) -> Snippet:
    result = await collection.find_one_and_update(
        {"_id": ObjectId(snippet.id)},
        {"$set": snippet_update.model_dump()},
        return_document=True
    )
    return result


@app.delete("/snippets/{snippet_id}", status_code=204)
async def delete_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]) -> None:
    await collection.delete_one({"_id": ObjectId(snippet.id)})
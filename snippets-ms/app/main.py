from typing import Optional
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId

MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
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

class Snippet(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    code: str

    model_config = ConfigDict(
        json_encoders = {
            PyObjectId: str
        },
        arbitrary_types_allowed=True,
        populate_by_name = True
    )


@app.get("/")
def status():
    return { "status": "OK" }


@app.post("/snippets")
async def upload_snippet(snippet: Snippet) -> Snippet:
    result =await collection.insert_one(snippet.model_dump())
    return await collection.find_one({"_id": result.inserted_id})


@app.get("/snippets")
async def all_snippets() -> list[Snippet]:
    return await collection.find().to_list()
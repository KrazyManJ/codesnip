from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, field_validator


class UploadSave(BaseModel):
    snippet_id: str

    @field_validator('snippet_id')
    def validate_object_id(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid id format')
        return v


class Save(UploadSave):
    saved_at: datetime = Field(default_factory=datetime.now)


class SaveStatusRequestBody(BaseModel):
    snippet_ids: list[str] = Field(..., max_length=100)
    
    
class SaveStats(BaseModel):
    save_count: int
    
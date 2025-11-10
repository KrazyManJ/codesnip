from datetime import datetime
from enum import Enum
from .object_id import ObjectIdBaseModel

from pydantic import BaseModel


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



class Snippet(UploadSnippet, ObjectIdBaseModel):
    pass
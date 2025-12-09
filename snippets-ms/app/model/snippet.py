from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import TypedDict

from .object_id import ObjectIdBaseModel


class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class UploadSnippet(BaseModel):
    title: str
    description: str
    code: str
    language: str
    created_at: datetime = Field(default_factory=datetime.now)
    visibility: Visibility = Visibility.PUBLIC


class SnippetDict():
    """
    Is used for return value of Snippet model, and for repository
    """
    _id: str
    title: str
    description: str
    code: str
    language: str
    created_at: str
    visibility: str


class Snippet(UploadSnippet, ObjectIdBaseModel):
    pass
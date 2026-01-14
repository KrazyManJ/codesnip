from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import TypedDict

from .object_id import ObjectIdBaseModel


class Visibility(str, Enum):
    PUBLIC = "public"
    PRIVATE = "private"


class User(BaseModel):
    id: str
    username: str
    email_hash: str


class UploadSnippet(BaseModel):
    title: str
    description: str
    code: str
    language: str
    visibility: Visibility = Visibility.PUBLIC


class SnippetDict(TypedDict):
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
    author: User
    created_at: datetime = Field(default_factory=datetime.now)
from typing import TypedDict
from .object_id import ObjectIdBaseModel

class SearchResult(ObjectIdBaseModel):
    title: str
    language: str
    match_preview: str
    

class SearchResultDict(TypedDict):
    _id: str
    title: str
    language: str
    match_preview: str
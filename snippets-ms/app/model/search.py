from typing import TypedDict
from pydantic import BaseModel

from .object_id import ObjectIdBaseModel


class SnippetSearchResult(ObjectIdBaseModel):
    title: str
    language: str
    
class MatchSearchResult(BaseModel):
    title: str
    description: str
    code: str

class SearchResult(BaseModel):
    snippet: SnippetSearchResult
    match: MatchSearchResult
    

class SearchResultDict(TypedDict):
    _id: str
    title: str
    language: str
    match_preview: str
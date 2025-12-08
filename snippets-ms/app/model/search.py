from .object_id import ObjectIdBaseModel

class SearchResult(ObjectIdBaseModel):
    title: str
    language: str
    match_preview: str
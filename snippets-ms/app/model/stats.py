from pydantic import BaseModel


class LangStat(BaseModel):
    lang: str
    snippets_count: int
    total_bytes: int
    
    
class Stats(BaseModel):
    total_snippets_count: int
    total_bytes: int
    languages_data: list[LangStat]

from fastapi import FastAPI, Query

from .routes import snippets_router
from .services import database
from .model.snippet import Snippet


app = FastAPI(
    title="CodeSnip Snippets API",
    summary="CodeSnip service to provide and manage snippets, with ability to search them as well.",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/"
    }
)


@app.get("/", tags=["Status"])
def status():
    return {"status": "OK"}


app.include_router(snippets_router.router)


@app.post("/search", tags=["Snippets"])
async def search(
    query: str = None, 
    language: str = Query(default=None, alias="lang")
) -> list[Snippet]:
    return await database.temp_search(query, language)


@app.get("/langs", tags=["Snippets"])
async def get_all_languages() -> list[str]:
    return await database.get_all_languages()
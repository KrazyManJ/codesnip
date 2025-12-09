from fastapi import FastAPI, Query
from fastapi.concurrency import asynccontextmanager

from .routes import snippets_router
from .services import snippet_service
from .init_db import seed_data
from .services.search_service import search_client
from .model.search import SearchResult

@asynccontextmanager
async def lifespan(app: FastAPI):
    await search_client.start()
    # await seed_data()
    yield
    await search_client.close()


app = FastAPI(
    title="CodeSnip Snippets API",
    summary="CodeSnip service to provide and manage snippets, with ability to search them as well.",
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/"
    },
    lifespan=lifespan
)


@app.get("/", tags=["Status"])
def status():
    return {"status": "OK"}


app.include_router(snippets_router.router)

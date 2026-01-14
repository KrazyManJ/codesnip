from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .routes import snippet_router
# from .init_db import seed_data_if_empty
from .connectors.grpc_search_connector import search_connector_client
from fastapi_pagination import add_pagination

@asynccontextmanager
async def lifespan(_: FastAPI):
    await search_connector_client.start()
    # await seed_data_if_empty()
    yield
    await search_connector_client.close()


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Status"])
def status():
    return {"status": "OK"}


app.include_router(snippet_router.router)
add_pagination(app)
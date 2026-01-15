from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from app.routes.saves_router import saves_router

app = FastAPI(
    title="CodeSnip Saves API",
    summary="""
        CodeSnip service to provide information about saved statuses of snippets. 
        
        Allows to save and unsave snippet as well as getting save stats about one snippet.
    """,
    version="1.0.0",
    license_info={
        "name": "MIT",
        "url": "https://mit-license.org/"
    },
)

# noinspection PyTypeChecker
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


app.include_router(saves_router)
add_pagination(app)

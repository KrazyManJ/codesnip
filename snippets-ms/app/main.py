from fastapi import FastAPI

from .routes import snippets_router


app = FastAPI()


@app.get("/")
def status():
    return {"status": "OK"}


app.include_router(snippets_router.router)

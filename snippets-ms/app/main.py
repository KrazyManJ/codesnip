from fastapi import FastAPI

from .routes import snippets_router


app = FastAPI()
app.include_router(snippets_router.router)


@app.get("/")
def status():
    return {"status": "OK"}

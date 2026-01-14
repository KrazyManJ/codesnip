from fastapi import APIRouter, BackgroundTasks, Depends, Query, status, HTTPException
from typing import Annotated

from ..model.snippet import Snippet, UploadSnippet, User
from ..model.search import SearchResult
from ..model.stats import Stats
from ..services import snippet_service
from ..dependencies import validate_snippet_id
from ..auth import get_current_user

router = APIRouter(tags=["Snippets"])

snippets_router = APIRouter(prefix="/snippets")


@snippets_router.post(
    path="",
    response_model=Snippet,
    status_code=201
)
async def upload_snippet(
    snippet: UploadSnippet,
    background_tasks: BackgroundTasks,
    user: Annotated[User, Depends(get_current_user)]
):
    full_snippet = Snippet(
        author=user,
        **snippet.model_dump()
    )
    
    return await snippet_service.add_snippet(full_snippet, background_tasks)


@snippets_router.get(
    path="", 
    response_model=list[Snippet]
)
async def all_snippets():
    return await snippet_service.get_all_snippets()


@snippets_router.get(
    path="/{snippet_id}",
    response_model=Snippet,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "When provided id is not in `ObjectId` format"},
        status.HTTP_404_NOT_FOUND: {"description": "When desired snippet by id was not found"}
    }
)
async def get_snippet(snippet: Annotated[Snippet, Depends(validate_snippet_id)]):
    return snippet


@snippets_router.put(
    path="/{snippet_id}",
    response_model=Snippet,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "When provided id is not in `ObjectId` format"},
        status.HTTP_404_NOT_FOUND: {"description": "When desired snippet by id was not found"}
    }
)
async def update_snippet(
    snippet: Annotated[Snippet, Depends(validate_snippet_id)],
    snippet_update: UploadSnippet,
    background_tasks: BackgroundTasks,
    user: Annotated[User, Depends(get_current_user)]
):
    if user.id != snippet.author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    
    return await snippet_service.update_snippet_by_id(snippet.id, snippet_update, background_tasks)


@snippets_router.delete(
    path="/{snippet_id}",
    status_code=204,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "When provided id is not in `ObjectId` format"},
        status.HTTP_404_NOT_FOUND: {"description": "When desired snippet by id was not found"}
    }
)
async def delete_snippet(
    snippet: Annotated[Snippet, Depends(validate_snippet_id)],
    background_tasks: BackgroundTasks,
    user: Annotated[User, Depends(get_current_user)]
):
    if user.id != snippet.author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to perform this action"
        )
    
    return await snippet_service.delete_snippet_by_id(snippet.id, background_tasks)


@router.post(
    path="/search",
    response_model=list[SearchResult]
)
async def search(
    query: str = None,
    language: str = Query(default=None, alias="lang")
):
    return await snippet_service.search(query, language)


@router.get(
    path="/langs",
    response_model=list[str]
)
async def get_all_languages():
    return await snippet_service.get_all_languages()


@router.get(
    path="/stats",
    response_model=Stats
)
async def get_snippet_statistics():
    return await snippet_service.get_stats()


router.include_router(snippets_router)

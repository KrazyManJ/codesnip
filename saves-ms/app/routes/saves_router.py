from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_pagination import Page

from ..model.save import UploadSave, Save
from ..model.user import User
from ..dependencies import get_current_user, get_save_service, verify_object_id
from ..services.save_service import SaveService

saves_router = APIRouter(prefix="/saves", tags=["Saves"])

@saves_router.post(
    path="",
    response_model=Save,
)
async def save_snippet(
    user: Annotated[User, Depends(get_current_user)],
    body: UploadSave,
    save_service: Annotated[SaveService, Depends(get_save_service)]
):
    return await save_service.save_snippet(user, body)


@saves_router.delete(
    path="/{snippet_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def unsave_snippet(
    user: Annotated[User, Depends(get_current_user)],
    snippet_id: Annotated[str, Depends(verify_object_id)],
    save_service: Annotated[SaveService, Depends(get_save_service)]
):
    return await save_service.unsave_snippet(user, snippet_id)


@saves_router.get(
    path="/me",
    response_model=Page[Save],
)
async def get_saves_of_current_user(
    user: Annotated[User, Depends(get_current_user)],
    save_service: Annotated[SaveService, Depends(get_save_service)]
):
    return await save_service.get_all_saves_of_user(user.id)


@saves_router.get(
    path="/{snippet_id}",
    response_model=Save,
)
async def get_snippet(
    user: Annotated[User, Depends(get_current_user)],
    snippet_id: Annotated[str, Depends(verify_object_id)],
    save_service: Annotated[SaveService, Depends(get_save_service)]
):
    save = await save_service.get_snippet(user, snippet_id)
    if not save:
        raise HTTPException(status_code=404, detail=f"Save not found")
    return save
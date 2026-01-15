from typing import Annotated

from fastapi import APIRouter, Depends, status

from ..model.save import UploadSave, Save
from ..model.user import User
from ..dependencies import get_current_user, get_save_service
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
    snippet_id: str,
    save_service: Annotated[SaveService, Depends(get_save_service)]
):
    return await save_service.unsave_snippet(user, snippet_id)


@saves_router.get(
    path="/saves/me"
)
async def get_saves_of_current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return
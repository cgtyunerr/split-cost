"""Group invitation http router."""
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field
from starlette import status

from app.api.dependencies import get_user, SessionDep
from app.modules.group.schemas import Invitations
from app.modules.group.src.service import InvitationService
from app.modules.group.src.factory import GroupFactory


class InviteBodyDependency(BaseModel):
    """Invite body."""
    target_user_id: int = Field(..., description="Invited user's id.")


invitation_service: InvitationService = GroupFactory.invitation()
group_invitation_router: APIRouter = APIRouter(
    prefix="/invitation",
    tags=["group-invitation"]
)


@group_invitation_router.post(
    path="/{group_id}/",
    summary="Invite people in group.",
    status_code=status.HTTP_201_CREATED,
)
async def invite_user(
    session: SessionDep,
    user_id: Annotated[int, Depends(get_user)],
    invite_body_dependency: InviteBodyDependency = Body(...),
    group_id: int = Path(..., description="Group id."),
):
    """Invite user."""
    await invitation_service.invite_people(
        user_id=user_id,
        target_user_id=invite_body_dependency.target_user_id,
        group_id=group_id,
        session=session
    )


@group_invitation_router.delete(
    path="/{group_id}/",
    summary="remove people in group.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    session: SessionDep,
    user_id: Annotated[int, Depends(get_user)],
    invite_body_dependency: InviteBodyDependency = Body(...),
    group_id: int = Path(..., description="Group id."),
):
    """Delete user."""
    await invitation_service.remove_people_to_group(
        user_id=user_id,
        target_user_id=invite_body_dependency.target_user_id,
        group_id=group_id,
        session=session
    )


@group_invitation_router.patch(
    path="/",
    summary="accept invitation.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def accept_invitation(
    user_id: Annotated[int, Depends(get_user)],
    session: SessionDep,
    invitation_id: int = Query(..., description="invitation id."),
):
    """Accept invitation."""
    await invitation_service.accept_invitation(
        user_id=user_id,
        invitation_id=invitation_id,
        session=session
    )


@group_invitation_router.get(
    path="/",
    summary="Get all invitations.",
    status_code=status.HTTP_200_OK,
    response_model=Invitations
)
async def get_all_invitations(
    user_id: Annotated[int, Depends(get_user)],
    session: SessionDep,
):
    """Get all invitations."""
    result = await invitation_service.get_invitations_by_person(
        user_id=user_id,
        session=session
    )
    return ORJSONResponse(
        content=jsonable_encoder(result)
    )

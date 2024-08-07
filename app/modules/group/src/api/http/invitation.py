"""Group invitation http router."""
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path, Body
from pydantic import BaseModel, Field
from starlette import status

from app.api.dependencies import get_user, SessionDep
from app.modules.group.src.service import InvitationService
from app.modules.group.src.factory import GroupFactory


class InviteBodyDependency(BaseModel):
    """Invite body."""
    target_user_id: int = Field(..., description="Invited user's id.")


class GroupIdPathDependency(BaseModel):
    """Group id path dependency."""
    group_id: int = Path(..., description="Group id.")

class InvitationIdQueryDependency(BaseModel):
    """Group id path dependency."""
    invitation_id: int = Query(..., description="invitation id.")


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
    user_id: Annotated[int, Depends(get_user)],
    invite_body_dependency: InviteBodyDependency = Body(...),
    group_id_dependency=Annotated[GroupIdPathDependency, Depends()],
    session=SessionDep,
):
    """Invite user."""
    await invitation_service.invite_people(
        user_id=user_id,
        target_user_id=invite_body_dependency.target_user_id,
        group_id=group_id_dependency.group_id,
        session=session
    )


@group_invitation_router.delete(
    path="/{group_id}/",
    summary="remove people in group.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: Annotated[int, Depends(get_user)],
    invite_body_dependency: InviteBodyDependency = Body(...),
    group_id_dependency=Annotated[GroupIdPathDependency, Depends()],
    session=SessionDep,
):
    """Delete user."""
    await invitation_service.remove_people_to_group(
        user_id=user_id,
        target_user_id=invite_body_dependency.target_user_id,
        group_id=group_id_dependency.group_id,
        session=session
    )


@group_invitation_router.patch(
    path="/",
    summary="accept invitation.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def accept_invitation(
    user_id: Annotated[int, Depends(get_user)],
    invitation_id_dependency=Annotated[InvitationIdQueryDependency, Depends()],
    session=SessionDep
):
    """Accept invitation."""
    await invitation_service.accept_invitation(
        user_id=user_id,
        invitation_id=invitation_id_dependency.invitation_id,
        session=session
    )


@group_invitation_router.get(
    path="/",
    summary="Get all invitations.",
    status_code=status.HTTP_200_OK,
    response_model=list[[int, int]]
)
async def get_all_invitations(
    user_id: Annotated[int, Depends(get_user)],
    session: SessionDep
):
    """Get all invitations."""
    result = await invitation_service.get_invitations_by_person(
        user_id=user_id,
        session=session
    )

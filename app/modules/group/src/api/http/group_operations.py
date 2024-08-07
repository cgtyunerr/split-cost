"""Group http api module."""
from typing import Annotated

from fastapi import APIRouter, Depends, Query, Path
from pydantic import BaseModel
from starlette import status

from app.api.dependencies import get_user, SessionDep
from app.modules.group.src.factory import GroupFactory
from app.modules.group.src.service import GroupOperationsService

group_operations_service: GroupOperationsService = GroupFactory.group_operations()

group_operations_router: APIRouter = APIRouter(
    prefix="/group-operations",
    tags=["group-operations"],
)


class DescriptionDependency(BaseModel):
    """Description dependency."""
    description: str = Query("", description="username keyword for search users.")


class GroupIdPathDependency(BaseModel):
    group_id: int = Path(...,description="Group id.")


@group_operations_router.post(
    path="/create/",
    summary="create new group.",
    status_code=status.HTTP_201_CREATED
)
async def create_group(
    user_id: Annotated[int, Depends(get_user)],
    description_dependency: Annotated[DescriptionDependency, Depends()],
    session: SessionDep,
):
    """Create group."""
    await group_operations_service.create_group(
        user_id=user_id,
        description=description_dependency.description,
        session=session
    )


@group_operations_router.delete(
    path="/delete/{group_id}/",
    summary="Delete group.",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_group(
    user_id: Annotated[int, Depends(get_user)],
    group_id_dependency: Annotated[GroupIdPathDependency, Depends()],
    session: SessionDep,
):
    """Delete group."""
    await group_operations_service.delete_group(
        user_id=user_id,
        group_id=group_id_dependency.group_id,
        session=session
    )

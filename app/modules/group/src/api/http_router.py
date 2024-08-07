"""Group http router module."""
from fastapi import APIRouter

from .http import group_operations_router, group_invitation_router

group_router: APIRouter = APIRouter(
    prefix="/group",
    tags=["group"]
)

group_router.include_router(group_operations_router)
group_router.include_router(group_invitation_router)
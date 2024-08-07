"""Permission manager module."""
from pydantic import validate_call, InstanceOf
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules import ForbiddenError
from app.modules.common import PermissionType, Service
from app.modules.group.models import UserGroup


class PermissionManager(Service):
    """Permission manager service.

    Methods:
        check_permission: check permission
    """

    @validate_call
    async def check_permission(
        self,
        user_id: int,
        group_id: int,
        permission_type: PermissionType,
        session: InstanceOf[AsyncSession]
    ) -> None:
        """Check permission.

        Arguments:
            user_id: related user id.
            group_id: related group id.
            permission_type: permission type
            session: database session

        Raises:
            ForbiddenError
        """
        result = await session.execute(select(UserGroup).filter(
                and_(
                    UserGroup.user_id == user_id,
                    UserGroup.group_id == group_id,
                    UserGroup.is_active
                )
            )
        )
        user = result.scalars().first()
        if user is None:
            raise ForbiddenError("Unauthorized process.")

        if permission_type == PermissionType.ADMIN:
            if user.role != permission_type:
                raise ForbiddenError("Unauthorized process.")

        elif permission_type == PermissionType.MAINTAINER:
            if user.role == PermissionType.OBSERVER:
                raise ForbiddenError("Unauthorized process.")

"""Group service module."""
from pydantic import validate_call, InstanceOf
from sqlalchemy import select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.common import Service, PermissionType, NotFoundError
from app.modules.permission_manager import permission_check
from app.modules.group.models import Group, UserGroup


class GroupOperationsService(Service):
    """Group service.

    Methods:
        create_group: create new group
        delete_group: delete existing group
    """

    @validate_call
    async def create_group(
        self,
        user_id: int,
        description: str,
        session: InstanceOf[AsyncSession]
    ) -> None:
        """Create Group.

        Arguments:
            description: group description.
            user_id: user id.
            session: database session
        """
        new_group = Group(
            description=description,
            is_active=True
        )
        session.add(new_group)
        await session.commit()
        await session.refresh(new_group)
        new_user = UserGroup(
            user_id=user_id,
            group_id=new_group.id,
            role="admin"
        )
        session.add(new_user)
        await session.flush()

    @validate_call
    async def delete_group(
        self,
        user_id: int,
        group_id: int,
        session: InstanceOf[AsyncSession]
    ):
        """Delete group.

        Arguments:
            user_id: the user id.
            group_id: group id.
            session: database session

        Raises:
            ForbiddenError
        """
        await permission_check(
            user_id=user_id,
            group_id=group_id,
            permission_type=PermissionType.ADMIN,
            session=session
        )

        group_result = await session.execute(select(Group).filter(
            and_(
                Group.id == group_id,
                Group.is_active
            )
        ))

        group = group_result.scalar_one_or_none()
        if group is None:
            raise NotFoundError("Group not found.")
        group.is_active = False
        stmt = delete(UserGroup).where(UserGroup.id == group_id)
        await session.execute(stmt)



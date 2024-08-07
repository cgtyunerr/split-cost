"""Group invitation service module."""
from pydantic import validate_call, InstanceOf
from sqlalchemy import select, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.common import Service, PermissionType, ConflictError, NotFoundError
from app.modules.group import permission_check
from app.modules.group.models import UserGroup


class InvitationService(Service):
    """Invitation service."""
    @validate_call
    async def invite_people(
        self,
        user_id: int,
        target_user_id: int,
        group_id: int,
        session: InstanceOf[AsyncSession]
    ):
        """Invite people."""
        await permission_check(
            user_id=user_id,
            group_id=group_id,
            permission_type=PermissionType.ADMIN,
            session=session
        )

        new_user = UserGroup(
            user_id=target_user_id,
            group_id=group_id,
            role="observer",
            is_active=False
        )
        session.add(new_user)
        try:
            await session.flush()

        except IntegrityError:
            raise ConflictError("This user is invited or already in group.")

    @validate_call
    async def remove_people_to_group(
        self,
        user_id: int,
        target_user_id: int,
        group_id: int,
        session: InstanceOf[AsyncSession]
    ):
        """Delete invited user or group member to group."""
        await permission_check(
            user_id=user_id,
            group_id=group_id,
            permission_type=PermissionType.ADMIN,
            session=session
        )

        result_query = await session.execute(select(UserGroup).filter(UserGroup.user_id == target_user_id))
        user = result_query.scalars().first()
        if user is None:
            NotFoundError("User not found.")
        await session.delete(user)

    @validate_call
    async def accept_invitation(
        self,
        user_id: int,
        invitation_id: int,
        session: InstanceOf[AsyncSession]
    ):
        """Accept invitation."""
        result_query = await session.execute(select(UserGroup).filter(
            and_(
                UserGroup.id == invitation_id,
                UserGroup.user_id == user_id,
                not UserGroup.is_active
            )
        ))
        user = result_query.scalars().first()
        if user is None:
            NotFoundError("Invitation not found.")

        user.is_active = True

    @validate_call
    async def get_invitations_by_person(
        self,
        user_id: int,
        session: InstanceOf[AsyncSession]
    ) -> list[int]:
        """Get invited group ids."""
        result_query = await session.execute(select(UserGroup).filter(
            and_(
                UserGroup.user_id == user_id,
                not UserGroup.is_active
            )
        ))
        users = result_query.scalars().all()
        if not users:
            NotFoundError("Invitations not found.")

        result: list[[int, int]] = []
        for user in users:
            result.append(
                (user.id, user.group_id)
            )
        return result

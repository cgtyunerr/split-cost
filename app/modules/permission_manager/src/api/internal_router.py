"""Common internal router."""
from pydantic import validate_call, InstanceOf
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.common import PermissionType
from app.modules.permission_manager.src.service import PermissionManager
from app.modules.permission_manager.src.factory import PermissionManagerFactory

permission_manager: PermissionManager = PermissionManagerFactory.permission_manager()


@validate_call
async def permission_check(
    user_id: int,
    group_id: int,
    permission_type: PermissionType,
    session: InstanceOf[AsyncSession]
):
    """Permission check internal api."""
    await permission_manager.check_permission(
        user_id=user_id,
        group_id=group_id,
        permission_type=permission_type,
        session=session
    )

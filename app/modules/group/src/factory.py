"""Group factory module."""
from functools import lru_cache

from .service import GroupOperationsService, InvitationService


class GroupFactory:
    """Group factory class."""
    @staticmethod
    @lru_cache(maxsize=1)
    def group_operations() -> GroupOperationsService:
        return GroupOperationsService()

    @staticmethod
    @lru_cache(maxsize=1)
    def invitation() -> InvitationService:
        return InvitationService()

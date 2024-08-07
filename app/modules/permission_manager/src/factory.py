"""Common factory."""
from functools import lru_cache

from app.modules.permission_manager.src.service import PermissionManager


class PermissionManagerFactory:
    """Common factory class."""
    @staticmethod
    @lru_cache(maxsize=1)
    def permission_manager() -> PermissionManager:
        return PermissionManager()

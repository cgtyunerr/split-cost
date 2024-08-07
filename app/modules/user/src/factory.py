"""User service factory."""
from functools import lru_cache

from .service import UserService


class UserFactory:
    """User factory class."""
    @staticmethod
    @lru_cache(maxsize=1)
    def user_service() -> UserService:
        return UserService()

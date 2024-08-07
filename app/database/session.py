"""Database session module."""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings

from .base_session import BaseSessionManager


class DatabaseSessionManager(BaseSessionManager):
    """Database session manager.

     Methods:
         get_session: Get a new db session.
     """

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide database session for transaction."""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception as exception:
                await session.rollback()
                raise exception from exception
            finally:
                await session.close()


database_session_manager: DatabaseSessionManager = DatabaseSessionManager(
    str(settings.DB.db_url)
)

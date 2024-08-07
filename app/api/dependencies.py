"""Common api dependencies."""
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import database_session_manager


oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="/user/login/")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Get a database session."""
    async with database_session_manager.get_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]


def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> int:
    """Get the current user id from the token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET)
        return payload["user_id"]

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

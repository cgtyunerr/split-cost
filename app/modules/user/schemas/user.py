"""User schemas module."""
from datetime import datetime
from typing import TypeAlias

from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    """Base user schema.

    Attributes:
        id: int
    """
    id: int


class UserGetSchema(BaseUserSchema):
    """Get user.

    Attributes:
        name: str
    """
    name: str


Users: TypeAlias = list[UserGetSchema]


class UserMeSchema(BaseUserSchema):
    """Get me.

    Attributes:
        email: str
        created_at: datetime
    """

    email: str
    created_at: datetime


class UserCreateSchema(BaseModel):
    """Create user schema.

    Attributes:
        username: str
        email: str
        password: str
    """
    username: str
    email: str
    password: str


class UserLoginSchema(BaseModel):
    """User login.

    Attributes:
        access_token: str
        token_type: str
    """
    access_token: str
    token_type: str

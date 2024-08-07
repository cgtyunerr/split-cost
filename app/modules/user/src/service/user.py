"""User service module."""
from datetime import datetime

from pydantic import validate_call, InstanceOf
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from app.modules import NotFoundError
from app.modules.common import Service, ConflictError
from app.modules.user.exceptions import LoginFailedError
from app.modules.user.models import User
from app.modules.user.schemas import Users, UserMeSchema, UserCreateSchema, UserLoginSchema, UserGetSchema
from .utils import hash_password, check_password
from app.config import settings


class UserService(Service):
    """User service.

    Methods:
        create_user: Register user.
        login: login user.
        get_me: return data about the user.
        get_users: get related users.
        update_email: update email
    """
    @validate_call
    async def create_user(
        self,
        create_schema: UserCreateSchema,
        session: InstanceOf[AsyncSession]
    ) -> None:
        """Create new user,

        Arguments:
            create_schema: UserCreateSchema
            session: Db session

        Raises:
            ConflictError
        """
        create_schema.password = hash_password(password=create_schema.password)
        new_user = User(**create_schema.model_dump())
        session.add(new_user)
        try:
            await session.flush()

        except IntegrityError:
            raise ConflictError("This email is already used.")

    @validate_call
    async def login(
        self,
        password: str,
        email: str,
        session: InstanceOf[AsyncSession]
    ) -> UserLoginSchema:
        """Login user.

        Arguments:
            password: user password
            email: username
            session: database session

        Return:
            UserLoginSchema

        Raises:
            LoginFailedError
        """
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalars().first()

        if user is None:
            raise LoginFailedError

        check_password(
            password=password,
            hashed_pw=user.password
        )

        return UserLoginSchema(
            access_token=jwt.encode({"user_id": user.id}, settings.JWT_SECRET),
            token_type="bearer"
        )

    @validate_call
    async def get_me(
        self,
        user_id: int,
        session: InstanceOf[AsyncSession]
    ) -> UserMeSchema:
        """Get me.

        Arguments:
            user_id: the user's id.
            session: database session
        """
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user is None:
            NotFoundError(user)

        return UserMeSchema(
            id=user_id,
            email=user.email,
            created_at=user.created_at
        )

    @validate_call
    async def get_users(
        self,
        keyword: str,
        session: InstanceOf[AsyncSession]
    ) -> Users:
        """Get users by keyword.

        Attributes:
            keyword: keyword
            session: database session

        Raises:
            NotFoundError

        Return:
            Users
        """
        query_result = await session.execute(
            select(User).where(User.username.ilike(f"%{keyword}%"))
        )

        users = query_result.scalars().all()
        result: Users = []
        for user in users:
            result.append(
                UserGetSchema(
                    id=user.id,
                    name=user.username
                )
            )

        if len(result) == 0:
            raise NotFoundError("Users not found.")

        return result

    @validate_call
    async def update_email(
        self,
        user_id: int,
        session: InstanceOf[AsyncSession],
        new_email: str
    ) -> None:
        """Update email.

        Attributes:
            user_id: The user id.
            session: database session.
            new_email: The new email.

        Raises:
            InvalidInputError
        """
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()

        if user is None:
            NotFoundError("User not found.")

        user.email = new_email


"""Http router for user module."""

from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from starlette import status

from app.api.dependencies import SessionDep, get_user
from app.modules.user.schemas import UserLoginSchema, UserCreateSchema, UserMeSchema, Users
from app.modules.user.src.factory import UserFactory
from app.modules.user.src.service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

user_service: UserService = UserFactory.user_service()


class KeywordDependency(BaseModel):
    """Keyword dependency."""
    keyword: str = Query("", description="username keyword for search users.")


class EmailDependency(BaseModel):
    """Email dependency."""
    email: str = Field(..., description="The new email.")


@user_router.post(
    path="/login/",
    summary="user login.",
    response_model=UserLoginSchema,
    status_code=status.HTTP_200_OK
)
async def login(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Login user."""
    result: UserLoginSchema = await user_service.login(
        email=form_data.username,
        password=form_data.password,
        session=session
    )
    return ORJSONResponse(
        content=jsonable_encoder(result)
    )


@user_router.post(
    path="/register/",
    summary="User register",
    status_code=status.HTTP_201_CREATED
)
async def register(
    session: SessionDep,
    create_schema: UserCreateSchema = Body(...)
):
    """User register."""
    await user_service.create_user(
        create_schema=create_schema,
        session=session
    )


@user_router.get(
    path="/me/",
    summary="Get own user.",
    status_code=status.HTTP_200_OK,
    response_model=UserMeSchema
)
async def get_me(
    session: SessionDep,
    user_id: Annotated[int, Depends(get_user)],
):
    result: UserMeSchema = await user_service.get_me(
        user_id=user_id,
        session=session
    )
    return ORJSONResponse(
        content=jsonable_encoder(result)
    )


@user_router.get(
    path="/get-users/",
    summary="Get users with keyword.",
    status_code=status.HTTP_200_OK,
    response_model=Users
)
async def get_users(
    session: SessionDep,
    keyword_dependency: Annotated[KeywordDependency, Depends()]
):
    """Get users."""
    result: Users = await user_service.get_users(
        session=session,
        keyword=keyword_dependency.keyword
    )
    return ORJSONResponse(
        content=jsonable_encoder(result)
    )


@user_router.patch(
    path="/update-email/",
    summary="Update email.",
    status_code=status.HTTP_204_NO_CONTENT
)
async def update_email(
    session: SessionDep,
    user_id: Annotated[int, Depends(get_user)],
    email_dependency: EmailDependency = Body(...)
):
    """Update email."""
    await user_service.update_email(
        user_id=user_id,
        session=session,
        new_email=email_dependency.email
    )

"""Base model for SQLAlchemy models."""
from sqlalchemy.orm import as_declarative

from app.modules.common.models import IDMixin, IsActiveMixin, TimeStampMixin


@as_declarative()
class Base:
    """Base class for models."""


class BaseModelWithID(Base, IDMixin):
    """Base class for models with id."""


class BaseModelWithIsActive(Base, IsActiveMixin):
    """Base class for models with is_active."""


class BaseModelWithTimeStamp(Base, TimeStampMixin):
    """Base class for models with timestamp."""


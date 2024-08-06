"""Base model for SQLAlchemy models."""
from sqlalchemy.orm import as_declarative

from app.modules.common.models import IDMixin, TimeStampMixin


@as_declarative()
class Base(IDMixin, TimeStampMixin):
    """Base class for models."""



"""Base model for SQLAlchemy models."""
from sqlalchemy.orm import as_declarative


@as_declarative()
class Base:
    """Base class for models."""

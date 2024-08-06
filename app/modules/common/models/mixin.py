"""Common mixin and custom base classes."""
import datetime
from typing import Annotated

from sqlalchemy import BIGINT, REAL, Boolean, DateTime, String
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column
from sqlalchemy.sql import func

# Types
serial_pk = Annotated[
    int,
    mapped_column(
        BIGINT,
        autoincrement=True,
        primary_key=True
    )
]
integer = Annotated[
    int,
    mapped_column(
        BIGINT,
        nullable=False,
    ),
]
real = Annotated[
    float,
    mapped_column(
        REAL,
        nullable=False,
    ),
]
boolean = Annotated[
    bool,
    mapped_column(
        Boolean, default=True,
        nullable=False
    )
]
text = Annotated[
    str,
    mapped_column(
        String,
        nullable=False
    )
]


class IDMixin:
    """Primary key mixin."""
    id: Mapped[serial_pk]


class IsActiveMixin:
    """is active mixin."""
    is_active: Mapped[boolean]


class TimeStampMixin:
    """Timestamp mixin."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


@declarative_mixin
class TableNameMixin:
    """Mixin for table name and schema."""

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name."""
        return cls.__name__.lower()


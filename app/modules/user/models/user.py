"""User database model."""
import re

from sqlalchemy import TEXT
from sqlalchemy.orm import Mapped, validates, mapped_column

from app.modules.common import InvalidInputError
from app.modules.common.models import IDMixin, TimeStampMixin, Base, text


class User(Base, IDMixin, TimeStampMixin):
    """User database model."""

    __tablename__ = "user"
    __table_args__ = {'schema': "user"}

    username: Mapped[text]
    password: Mapped[text]
    email: Mapped[str] = mapped_column(TEXT, unique=True, nullable=False)

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise InvalidInputError("Email is not valid.")
        return email

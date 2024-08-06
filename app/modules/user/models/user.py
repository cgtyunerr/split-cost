"""User database model."""
import re

from sqlalchemy.orm import Mapped, validates

from app.modules.common import InvalidInputError
from app.modules.common.models import IDMixin, IsActiveMixin, TimeStampMixin, Base, text


class User(Base, IDMixin, IsActiveMixin, TimeStampMixin):
    """User database model."""

    __tablename__ = "user"
    __table_args__ = {'schema': "user"}

    username: Mapped[text]
    password: Mapped[text]
    email: Mapped[text]

    @validates('email')
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise InvalidInputError("Email is not valid.")
        return email

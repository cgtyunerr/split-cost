from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped
from app.modules.common.models import Base, text, integer, IDMixin, IsActiveMixin


class UserGroup(Base, IDMixin, IsActiveMixin):
    """User Group database model."""

    __tablename__ = "user_group"
    __table_args__ = (
        UniqueConstraint('user_id', 'group_id'),
        {'schema': "group"},
    )

    user_id: Mapped[integer]
    group_id: Mapped[integer]
    role: Mapped[text]

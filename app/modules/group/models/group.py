"""Group database model."""

from sqlalchemy.orm import Mapped

from app.modules.common.models import IDMixin, TimeStampMixin, Base, text, IsActiveMixin


class Group(Base, IDMixin, TimeStampMixin, IsActiveMixin):
    """User database model."""

    __tablename__ = "group"
    __table_args__ = {'schema': "group"}

    description: Mapped[text]

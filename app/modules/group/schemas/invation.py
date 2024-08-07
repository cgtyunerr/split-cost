"""Invitation models."""
from typing import TypeAlias

from pydantic import BaseModel


class InvitationSchema(BaseModel):
    """Invitation response schema.

        Attributes:
            invitation_id: inv id.
            group_id: group id.
    """
    invitation_id: int
    group_id: int


Invitations: TypeAlias = list[InvitationSchema]
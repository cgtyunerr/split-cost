"""Permission type schema."""
from enum import Enum


class PermissionType(str, Enum):
    ADMIN = "admin"
    MAINTAINER = "maintainer"
    OBSERVER = "observer"

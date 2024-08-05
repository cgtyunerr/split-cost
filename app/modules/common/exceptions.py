"""Common exceptions."""


class InvalidInputError(ValueError):
    """Invalid input."""
    def __init__(self, name):
        """Throw exception."""
        super().__init__(f"Invalid {name}!")


class NotFoundError(ValueError):
    """Not found."""
    def __init__(self, name):
        """Throw exception."""
        super().__init__(f"{name.title()} not found!")


class ConflictError(ValueError):
    """Item conflict"""

    def __init__(self, name: str):
        """Throw exception."""
        super().__init__(f"{name.title()} already exists!")


class UnprocessableEntityError(ValueError):
    """Item is unprocessable."""

    def __init__(self, name: str):
        """Throw exception."""
        super().__init__(f"{name.title()} is unprocessable!")

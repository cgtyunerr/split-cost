"""User module exceptions."""


class LoginFailedError(ValueError):
    """Raises when credentials are not correct."""

    def __init__(self, message="Login credentials are not correct."):
        """Initialize the class."""
        self.message = message
        super().__init__(self.message)

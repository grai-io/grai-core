class NotSupportedError(Exception):
    """Raised when a feature is not supported by the client."""

    pass


class ObjectNotFoundError(ValueError):
    """Raised when a resource is not found."""

    pass


class InvalidResponseError(ValueError):
    """Raised when a response is not valid."""

    pass

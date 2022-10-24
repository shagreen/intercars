from rest_framework.exceptions import APIException


class ApplicationError(APIException):
    """Base application error class"""

    def __init__(self, message, extra=None):
        super().__init__(message)

        self.message = message
        self.extra = extra or {}

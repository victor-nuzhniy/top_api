"""Exceptions for 'service' app."""
from django.utils.encoding import force_str
from rest_framework import status
from rest_framework.exceptions import APIException


class CustomValidationError(APIException):
    """Custom validation error class."""

    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Not found."

    def __init__(self, detail, field, status_code):
        """Initialize custom validation class."""
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {field: force_str(detail)}
        else:
            self.detail = {"detail": force_str(self.default_detail)}

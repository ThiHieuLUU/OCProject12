from rest_framework.exceptions import APIException


class UniqueConstraint(APIException):
    """Class to generate exceptions for unique constraint."""

    status_code = 403
    default_detail = ""
    default_code = "Unique relation constraint"

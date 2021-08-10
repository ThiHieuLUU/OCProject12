from rest_framework.exceptions import APIException
from django.shortcuts import _get_queryset


class UniqueConstraint(APIException):
    """Class to generate exceptions for unique constraint."""

    status_code = 403
    default_detail = ""
    default_code = "Unique relation constraint"


class NotFound(APIException):
    """Class to generate exceptions for not found object."""

    status_code = 404
    default_detail = 'Not found'
    default_code = "error"


def get_object_or_404_error(klass, detail=None, *args, **kwargs):
    """
    Override the get_object_or_404
    """

    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise NotFound(detail=detail)

from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Client
from rest_framework.exceptions import APIException
from .admin import (
    ClientAdminConfig,
    ContractAdminConfig,
    EventAdminConfig,
)


class ModelPermission(BasePermission):
    """This permission controls the type of endpoints: /projects/{id}/issues/ or /projects/{id}/issues/{id}.
    - get_queryset method already checks permission for GET method.
    - "POST" method is needed to check permission for the nested relationship in the endpoint.
    - PUT/DELETE methods are needed to check permission because only author of an issue can do these actions.
    """

    message = 'Adding/Modifying/Deleting client is restricted to the member of sales team.'

    def __init__(self, model_admin_config=None):
        super(ModelPermission, self).__init__()
        self.model_admin_config = model_admin_config

    def has_permission(self, request, view):
        """
        Override has_permission method to treat the POST method.
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method == "POST":
            return self.model_admin_config.has_add_permission(self, request)
        return True

    def has_object_permission(self, request, view, obj):
        """
        Override has_object_permission method to treat PUT (for update) and DELETE methods.
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.method == "GET":
            return self.model_admin_config.has_view_permission(self, request, obj=obj)
        if request.method == "PUT":
            return self.model_admin_config.has_change_permission(self, request, obj=obj)
        if request.method == "DELETE":
            return self.model_admin_config.has_delete_permission(self, request, obj=obj)


class ClientPermission(ModelPermission):
    def __init__(self):
        super(ClientPermission, self).__init__(model_admin_config=ClientAdminConfig)

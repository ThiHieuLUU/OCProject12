from rest_framework.permissions import BasePermission, SAFE_METHODS
from .admin import (
    ClientAdminConfig,
    ContractAdminConfig,
    EventAdminConfig,
)


class ModelPermission(BasePermission):
    """To take the same permissions defined in admin configuration for a given model."""

    def __init__(self, model_admin_config=None):
        super(ModelPermission, self).__init__()
        self.model_admin_config = model_admin_config  # admin configuration for the model named "model"

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


class ContractPermission(ModelPermission):
    def __init__(self):
        super(ContractPermission, self).__init__(model_admin_config=ContractAdminConfig)


class EventPermission(ModelPermission):
    def __init__(self):
        super(EventPermission, self).__init__(model_admin_config=EventAdminConfig)

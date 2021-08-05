from django.db.models import Q
from django.contrib import admin
from ..models import (
    Client,
)

from ..user_role import (
    is_superuser_or_manager,
    is_seller,
    superuser_or_manager_permission
)


class ClientAdminConfig(admin.ModelAdmin):
    model = Client
    """Any seller can create (add) a client but only the main sales contact (main seller of this client) can update and
    delete this client """

    def get_queryset(self, request):
        """Sellers, supporters can see theirs own clients."""
        user = request.user
        if is_superuser_or_manager(user):
            return super(ClientAdminConfig, self).get_queryset(request)

        return Client.objects.filter(
            Q(main_sales_contact=user)
            | Q(contracts__sales_contact=user)
            | Q(contracts__event__support_contact=user)
        ).distinct()

    @superuser_or_manager_permission
    def has_add_permission(self, request):
        """Superuser, member of Managers group or Sellers group can add a client."""
        if is_seller(request.user):
            return True
        return False

    @superuser_or_manager_permission
    def has_view_permission(self, request, obj=None):
        """A seller or a supporter can only view theirs own clients."""
        user = request.user
        if obj and type(obj) is Client:
            return obj.is_user_in_sales_contacts_of_client(user) or obj.is_user_in_support_contacts_of_client(user)
        return True

    @superuser_or_manager_permission
    def has_change_permission(self, request, obj=None):
        """Superuser, member of Managers group can modify a client.
        Seller can modify a client if he is the main sales contact.
        """

        if type(obj) is Client:
            return obj.is_user_in_main_sales_contacts_of_client(request.user)
        return False

    @superuser_or_manager_permission
    def has_delete_permission(self, request, obj=None):
        """Superuser, member of Managers group can delete a client.
        Seller can delete a client if he is the main sales contact.
        """
        if type(obj) is Client:
            return obj.is_user_in_main_sales_contacts_of_client(request.user)
        return False

    @superuser_or_manager_permission
    def has_module_permission(self, request):
        if request.user.groups.filter(name__in=['Sellers', 'Supporters']).exists():
            return True
        return False

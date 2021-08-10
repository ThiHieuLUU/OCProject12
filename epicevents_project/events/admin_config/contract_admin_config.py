"""Configuration setup for admin page in order to allow who can access and perform CRUD operators on Contract model."""

from django.db.models import Q
from django.contrib import admin
from ..models import (
    Contract,
)

from ..user_role import (
    is_superuser_or_manager,
    is_seller,
    superuser_or_manager_permission
)


class ContractAdminConfig(admin.ModelAdmin):
    """Set view and CRUD permissions over the Client module for an authenticated user in the admin page.
    A superuser or a manager has all permissions.
    Sales group can create a contract. Only the main seller can delete this contract.
    The seller signs the contract and the main seller can view and update the contract.
    """

    def get_form(self, request, obj=None, **kwargs):
        """Allow to disable some fields which should not be modified."""

        form = super(ContractAdminConfig, self).get_form(request, obj, **kwargs)

        if type(obj) is Contract:
            # In order to update a contract which belongs to a client, the client field should not be changed.
            form.base_fields['client'].disabled = True
        return form

    def get_queryset(self, request):
        """Sellers can see only theirs own contracts."""
        user = request.user
        if is_superuser_or_manager(user):
            return super(ContractAdminConfig, self).get_queryset(request)

        return Contract.objects.filter(
            Q(sales_contact=user)
            | Q(client__main_sales_contact=user)
        ).distinct()

    @superuser_or_manager_permission
    def has_add_permission(self, request):
        """Superuser, member of Managers group or Sellers group can add a contract."""
        if is_seller(request.user):
            return True
        return False

    @superuser_or_manager_permission
    def has_view_permission(self, request, obj=None):
        """A seller can see only theirs own contracts."""
        user = request.user
        if obj and type(obj) is Contract:
            return obj.is_user_in_sales_contacts_of_contract(user)
        return True

    @superuser_or_manager_permission
    def has_change_permission(self, request, obj=None):
        """Superuser, member of Managers group can modify a contract.
        Seller can modify a contract if he is related to this contract (as main sales contact or sales contact).
        """
        if type(obj) is Contract:
            return obj.is_user_in_sales_contacts_of_contract(request.user)
        return False

    @superuser_or_manager_permission
    def has_delete_permission(self, request, obj=None):
        """Superuser, member of Managers group can delete a client.
        Seller can delete a contract if he is the main sales contact.
        """
        if type(obj) is Contract:
            return obj.is_user_in_main_sales_contacts_of_contract(request.user)
        return False

    @superuser_or_manager_permission
    def has_module_permission(self, request):
        """Superuser, member of Managers group can see the Contract model.
        Member of Sellers group also can this.
        """
        if request.user.groups.filter(name__in=['Sellers']).exists():
            return True
        return False

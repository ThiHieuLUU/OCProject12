from django.db.models import Q
from django.contrib import admin
from ..models import (
    Event
)

from ..user_role import (
    is_superuser_or_manager,
    is_seller,
    superuser_or_manager_permission
)


class EventAdminConfig(admin.ModelAdmin):
    """Sales group can create an event. Only the main seller can delete this event.
    The seller signs the contract and the main seller can view and update the event.
    """

    def get_form(self, request, obj=None, **kwargs):
        form = super(EventAdminConfig, self).get_form(request, obj, **kwargs)

        if type(obj) is Event:
            # In order to update an event coming from a contract, the contract field should not be changed.
            form.base_fields['contract'].disabled = True
        return form

    def get_queryset(self, request):
        """Sellers and supporters can see only theirs own events."""
        user = request.user
        if is_superuser_or_manager(user):
            return super(EventAdminConfig, self).get_queryset(request)

        return Event.objects.filter(
            Q(support_contact=user)
            | Q(contract__sales_contact=user)
            | Q(contract__client__main_sales_contact=user)
        ).distinct()

    @superuser_or_manager_permission
    def has_add_permission(self, request):
        """Superuser, member of Managers group or Sellers group can add an event."""
        if is_seller(request.user):
            return True
        return False

    @superuser_or_manager_permission
    def has_view_permission(self, request, obj=None):
        """A seller or a supporter can see only theirs own events."""
        user = request.user
        if obj and type(obj) is Event:
            return obj.is_user_in_sales_contacts_of_event(user) or obj.is_user_in_support_contacts_of_event(user)
        return True

    @superuser_or_manager_permission
    def has_change_permission(self, request, obj=None):
        """Superuser, member of Managers group can modify a event.
        Seller or supporter can modify an event if he is related to this event (as main sales contact or sales contact).
        """
        user = request.user
        if type(obj) is Event:
            return obj.is_user_in_sales_contacts_of_event(user) or obj.is_user_in_support_contacts_of_event(user)
        return False

    @superuser_or_manager_permission
    def has_delete_permission(self, request, obj=None):
        """Superuser, member of Managers group can delete a client.
        Seller can delete a event if he is the main sales contact.
        """
        if type(obj) is Event:
            return obj.is_user_in_main_sales_contacts_of_event(request.user)
        return False

    @superuser_or_manager_permission
    def has_module_permission(self, request):
        if request.user.groups.filter(name__in=['Sellers', 'Supporters']).exists():
            return True
        return False



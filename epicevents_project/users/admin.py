"""Configuration setup for admin page in order to allow who can access and perform CRUD operators for User model."""

from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.contrib import admin
from django.contrib.auth.backends import ModelBackend

from .models import User


class UserAdminConfig(UserAdmin, ModelBackend):
    """Set appearance for the user model in the admin page."""

    model = User
    search_fields = ('email', 'username', 'first_name', 'last_name',)
    list_filter = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff')
    ordering = ('-datetime_created',)
    list_display = ('email', 'username', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    # Fields displayed for update operator
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about',)}),
        ('Groups', {'fields': ('groups',)}),
    )
    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    # Fields displayed for create operator
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff',
                'about', 'groups')}
         ),
    )

    def has_module_permission(self, request):
        if request.user.is_superuser or request.user.groups.filter(name__in=['Managers']).exists():
            return True
        return False


# Add this configuration to admin site
admin.site.register(User, UserAdminConfig)

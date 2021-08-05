from .admin_config.client_admin_config import ClientAdminConfig
from .admin_config.contract_admin_config import ContractAdminConfig
from .admin_config.event_admin_config import EventAdminConfig
# from epicevents_project.events.admin_config.event_admin_config import EventAdminConfig
from django.contrib import admin
from .models import (
    Client,
    Contract,
    Event
)


admin.site.register(Client, ClientAdminConfig)
admin.site.register(Contract, ContractAdminConfig)
admin.site.register(Event, EventAdminConfig)


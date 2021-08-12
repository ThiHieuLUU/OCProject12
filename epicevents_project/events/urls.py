from django.urls import path, include
from rest_framework_nested import routers
from .views import (
    ClientViewSet,
    ContractViewSet,
    EventViewSet,
)

# See: https://github.com/alanjds/drf-nested-routers

# Generate:/clients/
# Generate:/clients/{client_pk}
router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet, basename='clients')

# Generate:/clients/{client_pk}/contracts/
# Generate:/clients/{client_pk}/contracts/{contract_pk}
clients_router = routers.NestedSimpleRouter(router, r'clients', lookup='client')
clients_router.register(r'contracts', ContractViewSet, basename='contracts')

# Generate:/clients/{client_pk}/contracts/{contract_pk}/events/
# Generate:/clients/{client_pk}/contracts/{contract_pk}/events/{event_pk}
contracts_router = routers.NestedSimpleRouter(clients_router, r'contracts', lookup='contract')
contracts_router.register(r'event', EventViewSet, basename='event')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(clients_router.urls)),
    path('', include(contracts_router.urls)),
]

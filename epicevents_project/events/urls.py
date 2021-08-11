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

# Generate: /contracts/
# Generate: /contracts/{contract_pk}
clients_router = routers.SimpleRouter()
clients_router.register(r'contracts', ContractViewSet, basename='contracts')

# Generate: /events/
# Generate: /events/{event_pk}
contracts_router = routers.SimpleRouter()
contracts_router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(clients_router.urls)),
    path('', include(contracts_router.urls)),
]
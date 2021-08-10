import django_filters
from django_filters import CharFilter, NumberFilter, DateTimeFilter
from .models import (
    Client,
    Contract,
    Event
)


class ClientFilter(django_filters.FilterSet):
    """Filters will be used with ClientViewSet."""
    first_name_contains = CharFilter(field_name="first_name", lookup_expr='icontains')
    last_name_contains = CharFilter(field_name="last_name", lookup_expr='icontains')
    email_contains = CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = Client
        fields = [
            'first_name',
            'first_name_contains',
            'last_name',
            'last_name_contains',
            'email',
            'email_contains'
        ]


class ContractFilter(django_filters.FilterSet):
    """Filters will be used with ContractViewSet."""
    client__first_name_contains = CharFilter(field_name="client__first_name", lookup_expr='icontains')
    client__last_name_contains = CharFilter(field_name="client__last_name", lookup_expr='icontains')
    client__email_contains = CharFilter(field_name="client__email", lookup_expr='icontains')
    amount_min = NumberFilter(field_name="amount", lookup_expr='gte')
    amount_max = NumberFilter(field_name="amount", lookup_expr='lte')
    date_created_min = DateTimeFilter(field_name='date_created', lookup_expr='gte')
    date_created_max = DateTimeFilter(field_name='date_created', lookup_expr='lte')

    class Meta:
        model = Contract
        fields = [
            'client__first_name',
            'client__first_name_contains',
            'client__last_name',
            'client__last_name_contains',
            'client__email',
            'client__email_contains',
            'date_created',
            'date_created_min',
            'date_created_max',
            'amount',
            'amount_min',
            'amount_max',

        ]


class EventFilter(django_filters.FilterSet):
    """Filters will be used with EventViewSet."""
    client__first_name = CharFilter(field_name="contract_client__first_name")
    client__first_name_contains = CharFilter(field_name="contract_client__first_name", lookup_expr='icontains')

    client__last_name_contains = CharFilter(field_name="contract_client__first_name")
    client__last_name_contains = CharFilter(field_name="contract_client__first_name", lookup_expr='icontains')

    client__email_contains = CharFilter(field_name="contract_client__first_name")
    client__email_contains = CharFilter(field_name="contract_client__first_name", lookup_expr='icontains')
    event_date = DateTimeFilter(field_name='event_date')

    class Meta:
        model = Event
        fields = [
            # 'client__first_name',
            # 'client__first_name_contains',
            # 'client__last_name',
            # 'client__last_name_contains',
            # 'client__email',
            # 'client__email_contains',
            'event_date'
        ]
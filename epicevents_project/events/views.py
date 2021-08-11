"""API Views for different requests about user, project, issue and comment.
"""
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.db import IntegrityError

from .models import (
    User,
    Client,
    Contract,
    Event
)
from .serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)
from .exceptions import UniqueConstraint, get_object_or_404_error
from .permissions import ClientPermission, ContractPermission, EventPermission
from .admin import ClientAdminConfig, ContractAdminConfig, EventAdminConfig
from .filters import ClientFilter, ContractFilter, EventFilter


class ClientViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """A viewset for viewing and editing client instances."""

    serializer_class = ClientSerializer
    permission_classes = [ClientPermission]
    filterset_class = ClientFilter

    def get_queryset(self):
        """Define a set of clients that the authenticated user can access."""
        return ClientAdminConfig.get_queryset(self, self.request)

    def create(self, request, *args, **kwargs):
        """Create a client."""

        # Pop all read-only data
        data = request.data
        main_sales_contact_data = data.pop("main_sales_contact", None)
        main_sales_contact = get_object_or_404_error(
            User,
            **main_sales_contact_data,
            detail="Main sales contact not found"
        )

        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(main_sales_contact=main_sales_contact)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update a client."""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        main_sales_contact_data = data.pop("main_sales_contact", None)
        main_sales_contact = get_object_or_404_error(
            User,
            **main_sales_contact_data,
            detail="Main sales contact not found"
        )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(main_sales_contact=main_sales_contact)

        return Response(serializer.data)


class ContractViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """ A viewset for viewing and editing contract instances."""

    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]
    filterset_class = ContractFilter

    def get_queryset(self):
        """Define a set of contracts that the authenticated user can access."""
        return ContractAdminConfig.get_queryset(self, self.request)

    def create(self, request, *args, **kwargs):
        """Create a contract."""

        # Pop all read-only data, here client and sales contact
        data = request.data

        client_data = data.pop("client", None)
        client = get_object_or_404_error(
            Client,
            **client_data,
            detail="Client not found"
        )

        sales_contact_data = data.pop("sales_contact", None)
        sales_contact = get_object_or_404_error(
            User,
            **sales_contact_data,
            detail="Sales contact not found"
        )

        serializer = ContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=client, sales_contact=sales_contact)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update a contract."""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        # If in the data has "client", pop it.
        # This field should not be modified because a contract is predetermined to belong to a unique client.
        data.pop("client", None)

        sales_contact_data = data.pop("sales_contact", None)
        sales_contact = get_object_or_404_error(
            User,
            **sales_contact_data,
            detail="Sales contact not found"
        )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(sales_contact=sales_contact)

        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing event instances."""

    serializer_class = EventSerializer
    permission_classes = [EventPermission]
    filterset_class = EventFilter

    def get_queryset(self):
        """Define a set of events that the authenticated user can access."""
        return EventAdminConfig.get_queryset(self, self.request)

    def create(self, request, *args, **kwargs):
        """Create an event."""

        data = request.data

        # Pop all read-only data
        # If in the data has "contract", pop it.
        # This field should not be modified because a contract signed is determined before making an event.
        contract_data = data.pop("contract", None)
        contract = get_object_or_404_error(
            Contract,
            **contract_data,
            detail="Contract not found"
        )

        support_contact_data = data.pop("support_contact", None)
        support_contact = get_object_or_404_error(
            User,
            **support_contact_data,
            detail="Support contact not found"
        )

        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(contract=contract, support_contact=support_contact)
        except IntegrityError:
            raise UniqueConstraint(detail="Unique constraint. An event is already created for this contract.")

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update an event."""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        # If in the data has "contract", pop it.
        # This field should not be modified because a contract signed is determined before making an event.
        data.pop("contract", None)

        support_contact_data = data.pop("support_contact", None)
        support_contact = get_object_or_404_error(
            User,
            **support_contact_data,
            detail="Support contact not found"
        )

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(support_contact=support_contact)

        return Response(serializer.data)

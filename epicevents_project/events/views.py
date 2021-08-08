"""API Views for different requests about user, project, issue and comment.
"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    User,
    Client,
    Contract,
)
from .serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)

from .permissions import ClientPermission, ContractPermission, EventPermission
from .admin import ClientAdminConfig, ContractAdminConfig, EventAdminConfig


class ClientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing client instances.
    """

    serializer_class = ClientSerializer
    permission_classes = [ClientPermission]
    # queryset = Client.objects.all()

    def get_queryset(self):
        """Define a set of clients that the authenticated user can access."""
        return ClientAdminConfig.get_queryset(self, self.request)

    def create(self, request, *args, **kwargs):
        """Create a client."""

        # Pop all read-only data
        data = request.data
        main_sales_contact_data = data.pop("main_sales_contact")
        main_sales_contact = get_object_or_404(User, **main_sales_contact_data)

        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(main_sales_contact=main_sales_contact)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update a client."""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        main_sales_contact_data = data.pop("main_sales_contact")
        main_sales_contact = get_object_or_404(User, **main_sales_contact_data)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(main_sales_contact=main_sales_contact)

        return Response(serializer.data)


class ContractViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing contract instances.
    """
    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]

    def get_queryset(self):
        """Define a set of contracts that the authenticated user can access."""
        return ContractAdminConfig.get_queryset(self, self.request)

    def create(self, request, *args, **kwargs):
        """Create a contract."""

        # Pop all read-only data
        data = request.data

        client_data = data.pop("client")
        client = get_object_or_404(Client, **client_data)

        sales_contact_data = data.pop("sales_contact")
        sales_contact = get_object_or_404(User, **sales_contact_data)

        serializer = ContractSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=client, sales_contact=sales_contact)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update a contract."""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        # If in the data has "user", pop it.
        # This field should not be modified because a contract is predetermined to belong to which client.
        data.pop("client", None)

        sales_contact_data = data.pop("sales_contact")
        sales_contact = get_object_or_404(User, **sales_contact_data)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(sales_contact=sales_contact)

        return Response(serializer.data)


class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing event instances.
    """
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    def get_queryset(self):
        """Define a set of events that the authenticated user can access."""
        return EventAdminConfig.get_queryset(self, self.request)

    def create(self, request, *args, **kwargs):
        """Create an event."""

        # Pop all read-only data
        data = request.data
        contract_data = data.pop("contract")
        contract = get_object_or_404(Contract, **contract_data)

        support_contact_data = data.pop("support_contact")
        support_contact = get_object_or_404(User, **support_contact_data)

        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(contract=contract, support_contact=support_contact)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update an event."""

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        data = request.data

        # If in the data has "contract", pop it.
        # This field should not be modified because a contract signed is determined before making an event.
        data.pop("contract", None)

        support_contact_data = data.pop("support_contact")
        support_contact = get_object_or_404(User, **support_contact_data)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save(support_contact=support_contact)

        return Response(serializer.data)

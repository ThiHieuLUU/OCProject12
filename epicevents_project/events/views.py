"""API Views for different requests about user, project, issue and comment.
"""
# from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.db import IntegrityError
from django.db.models import Q

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


class ClientViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    """
    A viewset for viewing and editing client instances.
    """

    serializer_class = ClientSerializer
    permission_classes = [ClientPermission]

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
    """
    A viewset for viewing and editing contract instances.
    """
    serializer_class = ContractSerializer
    permission_classes = [ContractPermission]

    def get_client_from_nested_endpoints(self):
        clients = ClientViewSet.get_queryset(self)

        client_pk = self.kwargs["client_pk"]
        client = get_object_or_404_error(
            clients,
            pk=client_pk,
            detail=f'Client not found with client_pk = {client_pk} and authenticated user: {self.request.user}'
        )
        return client

    def get_queryset(self):
        """Define a set of contracts that the authenticated user can access."""

        # Because with drf api, nested endpoints will be used so we can't use all get_queryset functions of admin
        # return ContractAdminConfig.get_queryset(self, self.request)

        client = self.get_client_from_nested_endpoints()
        contracts = client.contracts.all()
        return contracts

    def create(self, request, *args, **kwargs):
        """Create a contract."""

        # Pop all read-only data
        data = request.data
        data.pop("client", None)  # Don't take into account this information

        client = self.get_client_from_nested_endpoints()  # Also allow to check nested relationship

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

        # If in the data has "user", pop it.
        # This field should not be modified because a contract is predetermined to belong to which client.
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
    """
    A viewset for viewing and editing event instances.
    """
    serializer_class = EventSerializer
    permission_classes = [EventPermission]

    def get_contract_from_nested_endpoints(self):
        client = ContractViewSet.get_client_from_nested_endpoints(self)
        contract_pk = self.kwargs["contract_pk"]
        contract = get_object_or_404_error(
            Contract,
            pk=contract_pk,
            client=client,
            detail=f'Contract not found with contract_pk = {contract_pk} and client_pk = {client.pk}'
        )
        return contract

    # Because with drf api, nested endpoints will be used so we can't use all get_queryset functions of admin
    def get_queryset(self):
        """Define a set of events that the authenticated user can access."""
        contract = self.get_contract_from_nested_endpoints()
        # return contract.event
        return Event.objects.filter(pk=contract.pk)  # To have a queryset but not an instance

    def create(self, request, *args, **kwargs):
        """Create an event."""

        data = request.data

        # Pop all read-only data
        # If in the data has "contract", pop it.
        # This field should not be modified because a contract signed is determined before making an event.
        data.pop("contract", None)
        contract = self.get_contract_from_nested_endpoints()

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

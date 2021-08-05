"""API Views for different requests about user, project, issue and comment.
"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from django.db.utils import IntegrityError
from .exceptions import UniqueConstraint

from rest_framework.permissions import DjangoModelPermissions

from .models import (
    User,
    Client,
    Contract,
    Event,
)
from .serializers import (
    ClientSerializer,
    ContractSerializer,
    EventSerializer,
)

from .permissions import ClientPermission


class ClientViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing client instances.
    """

    serializer_class = ClientSerializer
    permission_classes = [ClientPermission]
    queryset = Client.objects.all()

    def create(self, request, *args, **kwargs):

        # Pop all read-only data
        data = request.data
        main_sales_contact_data = data.pop("main_sales_contact")
        main_sales_contact = get_object_or_404(User, **main_sales_contact_data)

        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(main_sales_contact=main_sales_contact)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
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
    queryset = Contract.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a contract"""

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
    A viewset for viewing and editing contract instances.
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()

    def create(self, request, *args, **kwargs):
        """Create a contract"""

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
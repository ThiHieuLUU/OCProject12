"""Serializers for some models: Client, Contract, Event."""

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import (
    Client,
    Contract,
    Event
)

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer is used for a user."""

    username = serializers.CharField(required=False, allow_blank=True)  # To get is_valid = True for unique field

    class Meta:
        model = User
        fields = ['id', 'username']
        read_only_fields = ['id']


class ClientSerializer(serializers.ModelSerializer):
    """Serializer is used for a client."""

    main_sales_contact = UserSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'company_name', 'is_official_client',
                  'main_sales_contact']
        read_only_fields = ['id']


class ContractSerializer(serializers.ModelSerializer):
    """Serializer is used for a contract."""

    sales_contact = UserSerializer(read_only=True)  # read_only=True whenever having a foreign key
    client = ClientSerializer(read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'client', 'sales_contact', 'is_signed', 'amount', 'payment_due', 'date_created']
        read_only_fields = ['id', 'date_created']


class EventSerializer(serializers.ModelSerializer):
    """Serializer is used for an event."""

    contract = ContractSerializer(read_only=True)  # read_only=True whenever having a foreign key
    support_contact = UserSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ['pk', 'contract', 'support_contact', 'status', 'attendees', 'event_date', 'notes']
        read_only_fields = ['pk']

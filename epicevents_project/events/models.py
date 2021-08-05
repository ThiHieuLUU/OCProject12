from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.db.models import Q

User = get_user_model()


class Client(models.Model):
    """Client model"""
    first_name = models.CharField(max_length=25, blank=False, null=False)
    last_name = models.CharField(max_length=25, blank=False, null=False)
    email = models.CharField(max_length=100, blank=False, null=False)
    # If seller is deleted, null will be set in sales_contact of a client.
    phone = models.CharField(max_length=20, null=False, blank=False)
    mobile = models.CharField(max_length=20, null=False, blank=False)
    company_name = models.CharField(max_length=250, null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_official_client = models.BooleanField(default=False)  # is potential or final client
    main_sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="clients")

    class Meta:
        app_label = 'events'
        verbose_name = 'client'
        verbose_name_plural = 'clients'

    def __str__(self):
        return f'Client\'s name: {self.first_name} {self.last_name}. Main seller: {self.main_sales_contact}'

    def is_user_in_main_sales_contacts_of_client(self, user):
        return user == self.main_sales_contact

    def is_user_in_sales_contacts_of_client(self, user):
        return user == self.main_sales_contact or self.contracts.filter(sales_contact=user).exists()

    # obj.contracts.filter(sales_contact=user) ok for for
    def is_user_in_support_contacts_of_client(self, user):
        if self.contracts.filter(event__support_contact=user).exists():
            return True
        return False


class Contract(models.Model):
    """ Contract model"""
    sales_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name="contracts")
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=False, related_name="contracts")
    date_created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True, null=False, blank=False)
    is_signed = models.BooleanField(default=False)  # status
    amount = models.FloatField(null=False, blank=False)
    payment_due = models.DateTimeField(null=False, blank=False)

    class Meta:
        app_label = 'events'
        verbose_name = 'contract'
        verbose_name_plural = 'contracts'

    def __str__(self):
        return f'Contract id: {self.id}. {self.client}. Signed with seller: {self.sales_contact}.'

    def is_user_in_main_sales_contacts_of_contract(self, user):
        return user == self.client.main_sales_contact

    def is_user_in_sales_contacts_of_contract(self, user):
        """A contract has one sales_contact (who signs the contract) and one main_sales_contact (related with client)"""
        # Method 1: takes more time with filter ?
        # client = self.client
        # return client.is_user_in_sales_contacts_of_client(self, user)

        # Method 2
        return user == self.sales_contact or user == self.client.main_sales_contact


class Event(models.Model):
    """Event model."""

    class StatusChoice(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        CANCELED = 'CANCELED', 'Canceled'
        IN_PROGRESS = 'IN PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    contract = models.OneToOneField(Contract, on_delete=models.CASCADE, primary_key=True, related_name="event")
    date_created = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    date_updated = models.DateTimeField(auto_now=True, null=False, blank=False)
    support_contact = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name="events")

    status = models.CharField(max_length=25, choices=StatusChoice.choices, default=StatusChoice.SCHEDULED)
    attendees = models.IntegerField(null=False, blank=False)
    event_date = models.DateTimeField(null=False, blank=False)
    notes = models.TextField(null=False, blank=False)

    class Meta:
        app_label = 'events'
        verbose_name = 'event'
        verbose_name_plural = 'events'

    def __str__(self):
        return f'Event id = {self.pk}. {self.contract} Supporter: {self.support_contact}'

    def is_user_in_main_sales_contacts_of_event(self, user):
        return user == self.contract.client.main_sales_contact

    def is_user_in_sales_contacts_of_event(self, user):
        contract = self.contract
        # Call the method checking user of contract because event and contract has one to one relationship.
        return contract.is_user_in_sales_contacts_of_contract(user)

    def is_user_in_support_contacts_of_event(self, user):
        return user == self.support_contact

from django.db import models

from cores.models import TimestampedModel
import uuid

class Address(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_id = models.CharField(max_length=255, blank=True, default=None, null=True)
    company = models.CharField(max_length=255, blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    street1 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class Parcel(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_id = models.CharField(max_length=255, blank=True, default=None, null=True)
    parcel_length = models.DecimalField(max_digits=12, decimal_places=3)
    parcel_width = models.DecimalField(max_digits=12, decimal_places=3)
    parcel_weight = models.DecimalField(max_digits=12, decimal_places=3)
    parcel_height = models.DecimalField(max_digits=12, decimal_places=3)
    distance_unit = models.CharField(max_length=255)
    mass_unit = models.CharField(max_length=255)

class Shipment(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_id = models.CharField(max_length=255, blank=True, default=None, null=True)
    address_from = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_from')
    address_to = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address_to')
    parcels = models.ManyToManyField(Parcel)

class Transaction(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    object_id = models.CharField(max_length=255, blank=True, default=None, null=True)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    carrier_account = models.CharField(max_length=255)
    servicelevel_token = models.CharField(max_length=255)

class ShippingMethod(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=3)
    currency = models.CharField(max_length=255, default='EUR')

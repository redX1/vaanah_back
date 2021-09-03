from django.db import models

from cores.models import TimestampedModel
import uuid

class Carrier(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# class Address(TimestampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     name = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
#     street1 = models.CharField(max_length=255)
#     city = models.CharField(max_length=255)
#     zip_code = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)

# class Parcel(TimestampedModel):
#     parcel_length = models.IntegerField()
#     parcel_width = models.IntegerField()
#     parcel_weight = models.IntegerField()
#     parcel_height = models.IntegerField()
#     distance_unit = models.CharField(max_length=255)
#     mass_unit = models.CharField(max_length=255)

# class Shipment(TimestampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     address_from = models.ForeignKey(Address, on_delete=models.CASCADE)
#     address_to = models.ForeignKey(Address, on_delete=models.CASCADE)
#     parcels = models.ManyToManyField(Parcel)

# class Transaction(TimestampedModel):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
#     carrier_account = models.CharField(max_length=255)
#     servicelevel_token = models.CharField(max_length=255)

class ShippingMethod(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=3)
    currency = models.CharField(max_length=255, default='EUR')

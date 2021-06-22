from django.db import models

from cores.models import TimestampedModel
import uuid


class ShippingMethod(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=15, decimal_places=3)
    currency = models.CharField(max_length=255)

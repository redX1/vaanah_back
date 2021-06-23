from django.conf import settings
from django.db import models
from cores.models import TimestampedModel
from orders.models import Order
import uuid

class PaymentModel(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.OneToOneField(Order, to_field='number', on_delete=models.CASCADE)
    method = models.CharField(max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=12, default='EUR')
    OPEN, DONE = (
        "open", 'done'
    )
    STATUS = [
        (OPEN, "open"),
        (DONE, "done")
    ]
    status = models.CharField(max_length=100, default=OPEN, choices=STATUS)

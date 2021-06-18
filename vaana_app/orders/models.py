from django.conf import settings
from django.db import models
from cores.models import TimestampedModel
import uuid
from carts.models import Cart
from addresses.models import Address
from shippings.models import ShippingMethod

class ShippingAddress(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=255)
    notes = models.TextField(blank=True, help_text="Tell us anything we should know when delivering your order.")
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

class Order(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=128, db_index=True, unique=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='orders',
        on_delete=models.SET_NULL
    )
    
    currency = models.CharField(max_length=12)
    total_tax = models.DecimalField(decimal_places=2, max_digits=12)
    shipping_tax = models.DecimalField(decimal_places=2, max_digits=12)
    total_prices = models.DecimalField(decimal_places=2, max_digits=12)

    INITIATED, CONFIRMED, SHIPPING, DELIVERED, CANCELED = (
        "initiated", "confirmed", "shipping", "delivered", "canceled"
    )
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE)

    # Use this field to indicate that an order is on hold / awaiting payment
    status = models.CharField(max_length=100, blank=True)

from django.conf import settings
from django.db import models
from cores.models import TimestampedModel
from products.models import Product
import uuid

class CartItem(TimestampedModel):
    """
    Cart item object
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1) 


class Cart(TimestampedModel):
    """
    Cart object
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name='carts',
        on_delete=models.CASCADE)

    # Cart statuses
    # - Frozen is for when a cart is in the process of being submitted
    #   and we need to prevent any changes to it.
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, ("Open - currently active")),
        (MERGED, ("Merged - superceded by another cart")),
        (SAVED, ("Saved - for items to be purchased later")),
        (FROZEN, ("Frozen - the cart cannot be modified")),
        (SUBMITTED, ("Submitted - has been ordered at the checkout")),
    )

    status = models.CharField(max_length=128, default=OPEN, choices=STATUS_CHOICES)

    merged_date = models.DateTimeField(null=True, blank=True)

    editable_statuses = (OPEN, SAVED)

    items = models.ManyToManyField(CartItem, blank=True)

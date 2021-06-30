from django.conf import settings
from django.db import models
from cores.models import TimestampedModel
from products.models import Product
import uuid

class WishListItem(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ('created_at',)

class WishList(TimestampedModel):
    """
    Cart object
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='wishlist', on_delete=models.CASCADE)

    items = models.ManyToManyField(WishListItem, blank=True)


from django.conf import settings
from django.db import models
from stores.models import Store
from categories.models import Category 
from cores.models import TimestampedModel


class Product(TimestampedModel):
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'


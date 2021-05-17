from django.conf import settings
from django.db import models
from categories.models import Category


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.ImageField(upload_to='test', blank=True, default='C:/Users/DELL/Downloads/image_not_found.jpg')
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('date_added',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'


from django.conf import settings
from django.db import models
from django.db.models.aggregates import Avg
from rest_framework.exceptions import ValidationError
from stores.models import Store
from categories.models import Category
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=3)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)
    quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    # review      = models.DecimalField(default=0.00,max_digits=100,decimal_places=2)
    class Meta:
        ordering = ('date_added',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    @property
    def no_of_ratings(self):
        sum=0
        reviews = Review.objects.filter(product=self)
        return len(reviews)

    # @property
    def avg_rating(self):
        sum=0
        reviews = Review.objects.filter(product=self)
        for review in reviews:
            sum=sum+review.rating

        if len(reviews)>0:
            return sum/len(reviews)
        else:
            return 0
    
    rating = property(avg_rating)


def validate_even(value):
    if value < 1 or value > 5 :
        raise ValidationError(
            ('%(value)s is not an valid rating'),
            params={'value': value},
        )
class Review(models.Model):
    title = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField(validators=[validate_even])
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

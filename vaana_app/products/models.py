from django.conf import settings
from django.db import models
from stores.models import Store
from categories.models import Category
from cores.models import TimestampedModel
import uuid
from files.models import File
from django.utils.text import slugify 
from django.utils.timezone import now

class Product(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=15, decimal_places=3)
    quantity = models.IntegerField()
    is_active = models.BooleanField()
    images = models.ManyToManyField(File)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    @property
    def no_of_ratings(self):
        sum=0
        reviews = ProductReview.objects.filter(product=self)
        return len(reviews)

    # @property
    def avg_rating(self):
        sum=0
        reviews = ProductReview.objects.filter(product=self)
        for review in reviews:
            sum=sum+review.rating

        if len(reviews)>0:
            return sum/len(reviews)
        else:
            return 0
    
    rating = property(avg_rating)

class ProductReview(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    comment = models.TextField()
    rating = models.IntegerField()
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title

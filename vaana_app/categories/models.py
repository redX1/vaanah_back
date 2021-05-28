from cores.models import TimestampedModel
from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Category(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=255)
    description = models.TextField() 
    slug        = models.SlugField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return f'/{self.slug}/'


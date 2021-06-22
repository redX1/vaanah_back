from cores.models import TimestampedModel
from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class Category(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name        = models.CharField(max_length=255, unique=True)
    description = models.TextField() 
    slug        = models.SlugField()
    parent      = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.CharField(max_length=255, default='test')


    class Meta:
        ordering = ('name',)
        unique_together = ('slug', 'parent',)    
        verbose_name_plural = "categories" 
    
    def __str__(self):                           
        full_path = [self.name]                  
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' -> '.join(full_path[::-1])


    def get_absolute_url(self):
        return f'/{self.slug}/'


from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name        = models.CharField(max_length=255)
    description = models.TextField() 
    slug        = models.SlugField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return f'/{self.slug}/'


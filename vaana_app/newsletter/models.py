from cores.models import TimestampedModel
from django.db import models
import uuid

# Create your models here.
class Newsletter(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255)

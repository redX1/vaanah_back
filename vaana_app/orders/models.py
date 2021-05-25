from django.conf import settings
from django.db import models
from cores.models import TimestampedModel
import uuid


class Order(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    number = models.CharField(max_length=128, db_index=True, unique=True)

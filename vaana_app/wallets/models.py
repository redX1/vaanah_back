from django.db import models
from cores.models import TimestampedModel
import uuid
from django.conf import settings

class Wallet(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

from django.conf import settings
from django.db import models
import uuid

from cores.models import TimestampedModel

class File(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        blank=True
    )
    file = models.FileField()
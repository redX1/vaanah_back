from django.db import models
from cores.models import TimestampedModel
import uuid

class Email(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # name = models.CharField(max_length=50)
    mail_to = models.EmailField(max_length=50)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)


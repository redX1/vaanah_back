from django.db import models
from django.utils import timezone
import uuid

class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    mail_to = models.EmailField(max_length=50)
    subject = models.CharField(max_length=200)
    body = models.TextField(max_length=2000)
    date_submitted = models.DateTimeField(default=timezone.now)


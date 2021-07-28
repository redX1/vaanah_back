from django.db import models
from django.db.models.fields.related import ManyToManyField
from cores.models import TimestampedModel
import uuid


class TopLevelDomain(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    domain = models.CharField(max_length=255)

class CallingCode(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255)

class Currency(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=255)

class Country(TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    top_level_domains =  models.ManyToManyField(TopLevelDomain, blank=True)
    calling_codes = models.ManyToManyField(CallingCode, blank=True)
    region = models.CharField(max_length=255)
    sub_region = models.CharField(max_length=255)
    currencies = models.ManyToManyField(Currency, blank=True)



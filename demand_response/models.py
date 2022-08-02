import datetime
from enum import Enum

from django.db import models
from django.utils import timezone


# ENUMs
class PriceItemType(Enum):
    GAS = "gas"
    ELECTRICITY = "electricity"

# Create your models here.
class PriceItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    date = models.DateTimeField()
    hour = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=5)
    type = models.CharField(max_length=15, choices=[(tag.name, tag.value) for tag in PriceItemType])

    class Meta:
        ordering = ['created']

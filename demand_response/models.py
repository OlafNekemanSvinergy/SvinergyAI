import datetime
from enum import Enum

from django.db import models
from django.utils import timezone


# ENUMs
class PriceItemType(models.TextChoices):
    GAS = "gas"
    ELECTRICITY = "electricity"


# Create your models here.
class PriceItem(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField()
    hour = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=5)
    type = models.CharField(max_length=15, choices=PriceItemType.choices)

    class Meta:
        ordering = ['created']

from enum import Enum

from django.db import models


# ENUMs
class HeatPumpBrand(Enum):
    BOSCH = "Bosch"
    VAILLANT = "Vaillant"


# Create your models here.
class HeatPump(models.Model):
    # Auto-generated fields
    created = models.DateTimeField(auto_now_add=True)

    # Attributes
    brand = models.CharField(max_length=15, choices=[(tag.name, tag.value) for tag in HeatPumpBrand])
    device_id = models.CharField(max_length=200, unique=True)
    serial_number = models.CharField(max_length=200, unique=True)

    max_power = models.IntegerField()

    class Meta:
        ordering = ['created']


class Connection(models.Model):
    # Auto-generated fields
    created = models.DateTimeField(auto_now_add=True)

    # Associations
    heat_pump = models.ForeignKey(HeatPump, on_delete=models.CASCADE)

    # Attributes
    brand = models.CharField(max_length=15, choices=[(tag.name, tag.value) for tag in HeatPumpBrand])
    access_token = models.CharField(max_length=2000)
    refresh_token = models.CharField(max_length=2000)
    valid_until = models.DateTimeField()
    valid = models.IntegerField()
    active = models.BooleanField(default=False)

    def is_active(self):
        return self.active == True

class DataPoint(models.Model):
    # Auto-generated fields
    timestamp = models.DateTimeField(auto_now_add=True)

    # Associations
    heat_pump = models.ForeignKey(HeatPump, on_delete=models.CASCADE)

    # Attributes
    temp_inside = models.DecimalField(max_digits=10, decimal_places=5)
    temp_set_point = models.DecimalField(max_digits=10, decimal_places=5)
    temp_range = models.DecimalField(max_digits=10, decimal_places=5)
    heating_on = models.BooleanField()
    power_level = models.DecimalField(max_digits=7, decimal_places=5)

    class Meta:
        ordering = ['timestamp']

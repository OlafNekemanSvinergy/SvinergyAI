import os
from datetime import datetime
import pytz
import requests
from http import HTTPStatus

from enum import Enum
from xml.dom.expatbuilder import parseString
from django.utils.translation import gettext_lazy as _
from django.db import models
from src.clients.vaillant import VaillantApi

# ENUMs
class HeatPumpBrand(models.TextChoices):
    BOSCH = 'Bosch', _('Bosch')
    VAILLANT = 'Vaillant', _('Vaillant')

class TokenType(models.TextChoices):
    BEARER = 'Bearer'
    BASIC = 'Basic'


# Create your models here.
class HeatPump(models.Model):
    # Auto-generated fields
    created = models.DateTimeField(auto_now_add=True)

    # Attributes
    brand = models.CharField(max_length=15, choices=HeatPumpBrand.choices)
    device_id = models.CharField(max_length=200, unique=True)
    serial_number = models.CharField(max_length=200, unique=True)

    max_power = models.IntegerField()

    def __str__(self):
        return self.brand + ' ' + str(self.id)

    class Meta:
        ordering = ['created']


class Connection(models.Model):
    # Auto-generated fields
    created = models.DateTimeField(auto_now_add=True)

    # Associations
    heat_pump = models.ForeignKey(HeatPump, on_delete=models.CASCADE)

    # Attributes
    brand = models.CharField(max_length=15, choices=HeatPumpBrand.choices)
    access_token = models.CharField(max_length=2000)
    refresh_token = models.CharField(max_length=2000)
    valid_until = models.DateTimeField()
    expires_in = models.IntegerField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'connection {id} - {brand} (Heat pump id: {heat_pump_id})'.format(
            id=self.id,
            brand=self.brand,
            heat_pump_id=self.heat_pump.id
        )

        # Class method

    def update_token_with_refresh_token(self):
        """
        Updates the connection with a new token using the refresh token.
        """
        token = None
        if self.brand == HeatPumpBrand.VAILLANT:
            token = VaillantApi.update_token_with_refresh_token(refresh_token=self.refresh_token)
        elif self.brand == HeatPumpBrand.BOSCH:
            token = None

        if token:
            self.access_token = token.access_token
            self.refresh_token = token.refresh_token
            self.valid_until = token.valid_until
            self.expires_in = token.expires_in
        else:
            self.active = False
        self.save()

    def update_system(self):
        """
        Retrieves a data point from the connection.
        """
        if datetime.now(pytz.utc) >= self.valid_until:
            # Get new token
            self.update_token_with_refresh_token()

        if self.brand == HeatPumpBrand.VAILLANT:
            # Update the Vaillant system

            url = 'https://api.vaillant-group.com/service-connected-control/states-api/v2/systems/{systemId}?includeMetadata=false'.format(
                systemId=self.heat_pump.device_id
            )
            headers = {
                'Content-Type': 'application/json',
                'Authorization': TokenType.BEARER + ' ' + self.access_token,
                'Ocp-Apim-Subscription-Key': os.getenv('VAILLANT_OCP_API_SUBSCRIPTION_KEY')
            }

            res = requests.get(url, headers=headers)
            if res.status_code == HTTPStatus.OK and os.getenv('VAILLANT_ENABLED'):
                data = res.json()
                data_point = DataPoint(
                    heat_pump=self.heat_pump,
                    temp_inside=data['centralHeating']['roomTemperature'],
                    temp_target=data['centralHeating']['roomTemperatureTarget'],
                    temp_range=0,
                    temp_outdoor=data['centralHeating']['outdoorTemperature'],
                    heating_on=False,
                    power_level=0
                )
                data_point.save()
            else:
                self.active = False
                self.save()
        elif self.brand == HeatPumpBrand.BOSCH:
            # Update the Bosch heat pump
            pass
        else:
            # Log message: brand not supported
            pass


class DataPoint(models.Model):
    # Auto-generated fields
    timestamp = models.DateTimeField(auto_now_add=True)

    # Associations
    heat_pump = models.ForeignKey(HeatPump, on_delete=models.CASCADE)

    # Attributes
    temp_inside = models.DecimalField(max_digits=10, decimal_places=5)
    temp_target = models.DecimalField(max_digits=10, decimal_places=5)
    temp_range = models.DecimalField(max_digits=10, decimal_places=5)
    temp_outdoor = models.DecimalField(max_digits=10, decimal_places=5)
    heating_on = models.BooleanField()
    power_level = models.DecimalField(max_digits=7, decimal_places=5)

    class Meta:
        ordering = ['timestamp']

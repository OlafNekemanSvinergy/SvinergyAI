from django.contrib import admin

from .models import HeatPump, Connection, DataPoint

# Register your models here.
admin.site.register([HeatPump, Connection, DataPoint])
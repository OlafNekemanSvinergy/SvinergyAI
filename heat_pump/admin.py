from django.contrib import admin

from .models import HeatPump, Connection, DataPoint

class DataPointAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'heat_pump', 'temp_inside', 'temp_target', 'temp_range', 'temp_outdoor', 'heating_on', 'power_level')

# Register your models here.
admin.site.register([HeatPump, Connection])
admin.site.register(DataPoint, DataPointAdmin)
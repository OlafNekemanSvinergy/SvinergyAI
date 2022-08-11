from django.contrib import admin

from .models import HeatPump, Connection, DataPoint

class DataPointAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'heat_pump', 'temp_inside', 'temp_target', 'temp_range', 'temp_outdoor', 'heating_on', 'power_level')

@admin.action(description='Manually update access token')
def manually_update_token(modeladmin, request, queryset):
    for query in queryset:
        query.update_token_with_refresh_token()

@admin.action(description='Manually fetch data point')
def update_system(modeladmin, request, queryset):
    for query in queryset:
        query.update_system()


class ConnectionAdmin(admin.ModelAdmin):

    actions = [manually_update_token, update_system]


# Register your models here.
admin.site.register(HeatPump)
admin.site.register(Connection, ConnectionAdmin)
admin.site.register(DataPoint, DataPointAdmin)
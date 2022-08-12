from urllib.parse import ParseResultBytes
from django.contrib import admin
from demand_response.energy_prices.frank_energie import *
from .models import PriceItem

@admin.action(description='Manually import Frank Energie prices')
def manual_fetch_frank_energie_prices(modeladmin, request, queryset):
    get_energy_prices()

class PriceItemAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'hour', 'price']
    ordering = ['-timestamp']
    actions = [manual_fetch_frank_energie_prices]


# Register your models here.
admin.site.register(PriceItem, PriceItemAdmin)

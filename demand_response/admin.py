from django.contrib import admin

from .models import PriceItem


class PriceItemAdmin(admin.ModelAdmin):
    list_display = ['date', 'hour', 'price']


# Register your models here.
admin.site.register(PriceItem, PriceItemAdmin)

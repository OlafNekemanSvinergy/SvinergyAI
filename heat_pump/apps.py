from django.apps import AppConfig


class HeatPumpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'heat_pump'

    def ready(self):
        from heat_pump import temperature_updater
        temperature_updater.start()
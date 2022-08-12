from heat_pump.models import Connection
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def get_temperatures():
    connection_list = Connection.objects.filter(active=True)
    for conn in connection_list:
        conn.update_system()

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_temperatures, trigger='cron', minute='*/5')
    scheduler.start()

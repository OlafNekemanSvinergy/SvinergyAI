import requests
from http import HTTPStatus
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from demand_response.models import PriceItem, PriceItemType


def get_frank_energie_start_date():
    """
    Fetches the start date for the Frank Energie electricity prices call
    """
    latest_price_item = PriceItem.objects.order_by('-timestamp').first()
    if latest_price_item:
        return latest_price_item.timestamp
    else:
        return datetime.now()


def get_energy_prices():
    start_date = get_frank_energie_start_date()
    tomorrow = start_date + timedelta(days=2)

    data = get_electricity_prices(
        start_date=start_date,
        end_date=tomorrow
    )
    if data:
        for item in data['data']['marketPricesElectricity']:
            timestamp = datetime.strptime(item['from'], '%Y-%m-%dT%H:%M:%S.%f%z')
            if PriceItem.objects.filter(timestamp=timestamp).exists():
                pass
            else:
                p = PriceItem(
                    timestamp=timestamp,
                    hour=timestamp.hour,
                    price=item['marketPrice'],
                    type=PriceItemType.ELECTRICITY
                )
                if p:
                    p.save()
    return True

def get_electricity_prices(start_date, end_date):
    """
    Fetches the electricity prices from the Frank Energie api.
    """
    yesterday = start_date + timedelta(days=-1)
    yesterday_string = yesterday.strftime("%Y-%m-%d")
    end_date_string = end_date.strftime("%Y-%m-%d")
    headers = {"content-type": "application/json"}
    query = f"""query MarketPrices {{
        marketPricesElectricity(startDate: "{yesterday_string}", endDate: "{end_date_string}") {{
        till
        from
        marketPrice
        priceIncludingMarkup
        }}
    }}"""
    response = requests.post('https://graphcdn.frankenergie.nl', json={'query': query}, headers=headers)
    if response.status_code == HTTPStatus.OK:
        return response.json()
    return None

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_energy_prices, 'interval', days=1)
    scheduler.start()

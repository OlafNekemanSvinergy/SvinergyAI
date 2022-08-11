"""
This file holds the Vaillant API client.
"""
# Packages
import os
import requests
from http import HTTPStatus
from datetime import datetime, timedelta

# Within module
from src.clients.api_response import Token, HeatPump, HeatPumpData


class VaillantApi:
    class API:
        AUTH = 'uaa/oauth'
        CONSUMPTION = 'consumption-api/v1'
        NOTIFICATION = ''
        PRODUCT_IDENTIFICATION = 'product-identification-api/v1'
        SCHEDULES = 'schedules-api/v2'
        SETTINGS = 'service-connected-control/settings-api/v2'
        STATES = 'service-connected-control/states-api/v2'
        SYSTEM_REGISTRATION = 'system-registration-api-with-consent/v1'
        SYSTEMS = 'service-connected-control/systems-api/v1'

    base_url = 'https://api.vaillant-group.com'

    headers = {
        'Ocp-Apim-Subscription-Key': os.getenv(
            'VAILLANT_OCP_API_SUBSCRIPTION_KEY')
    }

    @staticmethod
    def make_url(api, endpoint):
        """
        Builds the url for a Vaillant api call.
        """
        return '{}/{}/{}'.format(VaillantApi.base_url, api, endpoint)

    @staticmethod
    def update_token_with_refresh_token(refresh_token: str):
        """
        Fetches a new access token with
        """
        # Build url
        url = VaillantApi.make_url(api=VaillantApi.API.AUTH, endpoint='token')

        # Create headers
        headers = VaillantApi.headers.copy()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        if 'Bearer ' in refresh_token:
            headers['Authorization'] = refresh_token
        else:
            headers['Authorization'] = 'Bearer ' + refresh_token

        # Request body
        data = {'grant_type': 'refresh_token'}

        # Process request
        res = requests.post(url, headers=headers, data=data)

        if res.status_code == HTTPStatus.OK:
            content = res.json()
            return Token(
                access_token=content['access_token'],
                refresh_token=content['refresh_token'],
                expires_in=content['expires_in'],
                valid_until=datetime.now() + timedelta(
                    seconds=content['expires_in'])
            )

        return None

    @staticmethod
    def fetch_heat_pump_data(device_id, access_token):
        """
        Fetches the heat pump data needed for analysis.
        """
        # Create the url
        endpoint = 'systems/{}'.format('21202000201972220932005803N0')

        url = VaillantApi.make_url(
            api=VaillantApi.API.STATES,
            endpoint=endpoint
        )

        # Create headers
        headers = VaillantApi.headers.copy()
        headers['Authorization'] = access_token

        # Process request
        res = requests.get(url, headers=headers)

        if res.status_code == HTTPStatus.OK:
            content = res.json()
            t_data = HeatPumpData(
                temp_inside=content['centralHeating']['roomTemperature'],
                temp_target=content['centralHeating']['roomTemperatureTarget'],
                temp_range=0,
                temp_outdoor=content['centralHeating']['outdoorTemperature'],
                heating_on=False,
                power_level=0
            )
            return t_data

        return None

    @staticmethod
    def get_system_info(device_id, access_token):
        """
        Fetches the heat pump system information.
        """
        # Update the Vaillant system
        endpoint = 'systems/{systemId}?includeMetadata=false'.format(
            systemId=device_id
        )
        url = VaillantApi.make_url(
            api=VaillantApi.API.SYSTEMS,
            endpoint=endpoint
        )

        # Create headers
        headers = VaillantApi.headers.copy()
        headers['Authorization'] = access_token

        # Process request
        res = requests.get(url, headers=headers)

        if res.status_code == HTTPStatus.OK:
            content = res.json()
            gateway = content['devices']['gateway']
            heat_pump = HeatPump(
                device_id=gateway['serialNumber'],
                serial_number=gateway['serialNumber']
            )
            return heat_pump

        return None
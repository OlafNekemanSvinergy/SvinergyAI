"""
This file holds the Vaillant API client.
"""

import os
import requests
from http import HTTPStatus
from datetime import datetime, timedelta
from src.clients.api_response import Token


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
        'Ocp-Apim-Subscription-Key': os.getenv('VAILLANT_OCP_API_SUBSCRIPTION_KEY')
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
                valid_until=datetime.now() + timedelta(seconds=content['expires_in'])
            )
        return None

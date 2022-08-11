from rest_framework.parsers import JSONParser
import os
from typing import Union, Tuple

from django.http import Http404
from django.core import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat_pump.models import Connection
from heat_pump.serializers import ConnectionSerializer
import requests
from http import HTTPStatus
from urllib.parse import urljoin
from heat_pump.models import HeatPump, HeatPumpBrand, TokenType

from src.clients.vaillant import VaillantApi

class ConnectionList(APIView):
    """
    List all code connections, or create a new connection.
    """
    def get_object(self, device_id):
        try:
            return Connection.objects.get(device_id=device_id)
        except Connection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):
        serializer = ConnectionSerializer(data=request.data)

        if serializer.is_valid():
            heat_pump, created = register_system(conn=serializer)
            
            if heat_pump:
                if hasattr(heat_pump, "connection"):
                    self.update_tokens(conn=heat_pump.connection, data=request.data)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    serializer.save(heat_pump=heat_pump)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get_object(self, device_id):
    #     try:
    #         return ConnectionSerializer.objects.get(device_id=device_id)
    #     except ConnectionSerializer.DoesNotExist:
    #         raise Http404

    def update_tokens(self, conn, data):
        """
        Updates the access and refresh token. 
        """
        serializer = ConnectionSerializer(conn, data=data)
        if serializer.is_valid():
            serializer.save()
            return True
        return False           


class ConnectionDetail(APIView):
    """
    Retrieve, update or delete a code connections.
    """
    def get_object(self, device_id):
        try:
            return Connection.objects.get(device_id=device_id)
        except Connection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, device_id, format=None):
        connection = self.get_object(device_id=device_id)
        serializer = ConnectionSerializer(connection)
        return Response(serializer.data)

    def put(self, request, device_id, format=None):
        connection = self.get_object(device_id=device_id)
        serializer = ConnectionSerializer(connection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, device_id, format=None):
        connection = self.get_object(device_id=device_id)
        connection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



        
def register_system(conn: ConnectionSerializer) -> tuple[HeatPump, bool]:
    """
    Register the heat pump system.
    """ 
    if conn.validated_data.get('brand') == HeatPumpBrand.BOSCH:
        base_url = 'https://ews-emea.api.bosch.com/home/sandbox/pointt/v1/'
        endpoint = 'gateways'
        url = urljoin(base_url, endpoint)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': conn.validated_data.get('access_token')
        }

        res_gateways = requests.get(url, headers=headers)

        if res_gateways.status_code == HTTPStatus.OK:
            # create heat pump object
            gateways = res_gateways.json()

            res_system = requests.get(urljoin(url + '/', gateways[0]['deviceId']), headers=headers)
            data_system = res_system.json()
            heat_pump, created = HeatPump.objects.get_or_create(
                device_id=data_system['deviceId'], 
                defaults={'serial_number': data_system['serialNumber'], 'brand': HeatPumpBrand.BOSCH,
                'max_power': 2000}
                )
            if created:
                heat_pump.save()
            return heat_pump, created
        else:
            return None, None

    elif conn.validated_data.get('brand') == HeatPumpBrand.VAILLANT:    
        # Setup Vaillant system
        # Todo: fetch gateway number with api endpoint
        system = VaillantApi.get_system_info(
            device_id=conn.validated_data.get('device_id'),
            access_token=TokenType.BEARER + ' ' + conn.validated_data.get('access_token')
        )
        if system:
            heat_pump, created = HeatPump.objects.get_or_create(
                serial_number=system.serial_number,
                defaults={'brand': HeatPumpBrand.VAILLANT,
                'max_power': 2000}
                )
            if created:
                heat_pump.save()

            return heat_pump, created
    
    return None, False



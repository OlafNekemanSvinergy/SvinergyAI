from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat_pump.models import Connection
from heat_pump.serializers import ConnectionSerializer
import requests
from http import HTTPStatus
from urllib.parse import urljoin
from heat_pump.models import HeatPump, HeatPumpBrand

# Create your views here.
@api_view(['GET', 'POST'])
def connection_list(request, format=None):
    """
    List all code connections, or create a new connection.
    """
    if request.method == 'GET':
        connections = Connection.objects.all()
        serializer = ConnectionSerializer(connections, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ConnectionSerializer(data=request.data)
        if serializer.is_valid():
            heat_pump, created = setup_system(conn=serializer)
            if heat_pump and created:
                serializer.save(heat_pump=heat_pump)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def setup_system(conn: ConnectionSerializer):
    """
    Run a 
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
        elif conn.validated_data.get('brand') == HeatPumpBrand.VAILLANT:
            # Setup Vaillant system
            pass
        else:
            return None, None

@api_view(['GET', 'PUT', 'DELETE'])
def connection_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code connections.
    """
    try:
        connections = Connection.objects.get(pk=pk)
    except Connection.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ConnectionSerializer(connections)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ConnectionSerializer(connections, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        connections.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

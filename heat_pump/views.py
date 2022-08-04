from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat_pump.models import Connection
from heat_pump.serializers import ConnectionSerializer

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
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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
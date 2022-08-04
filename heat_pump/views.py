from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from heat_pump.models import Connection
from heat_pump.serializers import ConnectionSerializer

# Create your views here.
@csrf_exempt
def connection_list(request):
    """
    List all connections, or create a new connection.
    """
    if request.method == 'GET':
        connections = Connection.objects.all()
        serializer = ConnectionSerializer(connections, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ConnectionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def connection_detail(request, pk):
    """
    Retrieve, update or delete a code connection.
    """
    try:
        connection = Connection.objects.get(pk=pk)
    except Connection.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ConnectionSerializer(connection)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ConnectionSerializer(connection, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        connection.delete()
        return HttpResponse(status=204)
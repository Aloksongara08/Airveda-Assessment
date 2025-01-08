from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Device, TemperatureReading, HumidityReading
from .serializers import DeviceSerializer, TemperatureReadingSerializer, HumidityReadingSerializer
from django.shortcuts import render

class DeviceCreateView(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceDeleteView(generics.DestroyAPIView):
    queryset = Device.objects.all()
    lookup_field = 'uid'


class DeviceRetrieveView(generics.RetrieveAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = 'uid'


class DeviceListView(generics.ListAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

def device_graph(request):
    uid = request.GET.get('uid')
    parameter = request.GET.get('parameter')
    readings = TemperatureReading.objects.filter(device__uid=uid) if parameter == 'temperature' else HumidityReading.objects.filter(device__uid=uid)
    context = {'readings': list(readings.values('timestamp', 'value'))}
    return render(request, 'graph.html', context)


@api_view(['GET'])
def get_readings(request, uid, parameter):
    device = get_object_or_404(Device, uid=uid)
    start_on = request.GET.get('start_on')
    end_on = request.GET.get('end_on')

    if not (start_on and end_on):
        return Response({"error": "start_on and end_on query parameters are required."}, status=status.HTTP_400_BAD_REQUEST)

    if parameter == "temperature":
        readings = TemperatureReading.objects.filter(device=device, timestamp__range=[start_on, end_on])
        serializer = TemperatureReadingSerializer(readings, many=True)
    elif parameter == "humidity":
        readings = HumidityReading.objects.filter(device=device, timestamp__range=[start_on, end_on])
        serializer = HumidityReadingSerializer(readings, many=True)
    else:
        return Response({"error": "Invalid parameter. Use 'temperature' or 'humidity'."}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data)


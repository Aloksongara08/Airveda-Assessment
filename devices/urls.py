from django.urls import path
from .views import (
    DeviceCreateView,
    DeviceDeleteView,
    DeviceRetrieveView,
    DeviceListView,
    get_readings,
    device_graph,
)

urlpatterns = [
    path('api/devices/', DeviceCreateView.as_view(), name='create-device'),
    path('api/devices/<str:uid>/', DeviceRetrieveView.as_view(), name='retrieve-device'),
    path('api/devices/<str:uid>/delete/', DeviceDeleteView.as_view(), name='delete-device'),
    path('api/devices/list/', DeviceListView.as_view(), name='list-devices'),
    path('api/devices/<str:uid>/readings/<str:parameter>/', get_readings, name='get-readings'),
    path('devices-graph/', device_graph, name='device-graph'),
]

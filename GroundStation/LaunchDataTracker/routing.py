from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/telemetry/(?P<payload_name>\w+)/send$', consumers.TelemetryConsumer.as_asgi()),
    re_path(r'ws/telemetry/(?P<payload_name>\w+)/receive$', consumers.ClientConsumer.as_asgi()),
    re_path(r'ws/peripheral/(?P<peripheral_name>\w+)/(?P<sender_name>\w+)$', consumers.PeripheralConsumer.as_asgi()),
]
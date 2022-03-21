from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.index),
    path('payload/<slug:payload_id>/send_packet',views.send_telemetry),
    path('client/<int:launch_id>/get_last_packet',views.get_telemetry),
]
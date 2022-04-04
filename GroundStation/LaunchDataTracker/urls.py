from django.urls import URLPattern, path,include

from . import views

urlpatterns = [
    path('', views.index),
    path('peripheral/<slug:peripheral_id>/get_active_launches', views.get_peripheral_launches),
    path('payload/<slug:payload_id>/send_packet',views.send_telemetry),
    path('client/<int:launch_id>/get_last_packet',views.get_telemetry),
]
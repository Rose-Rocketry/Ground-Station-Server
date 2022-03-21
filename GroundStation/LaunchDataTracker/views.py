from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *

# Create your views here.
@csrf_exempt
def send_telemetry(req, payload_id):
    '''Temporary Send Data'''
    if req.method == "GET":
        return HttpResponse("🎉 You should not be seeing this. XP")
    try:
        launch = LaunchInfo.objects.get(flight_computer=payload_id, active_launch=True)
        data = json.loads(req.body)
        TelemetryPacket.objects.create(telemetry = data, launch=launch)
    except LaunchInfo.DoesNotExist:
        pass
    return HttpResponse()

def get_telemetry(req, launch_id):
    '''Temporary Get Data'''
    try:
        launch = LaunchInfo.objects.get(pk=launch_id)
        latest_packet = TelemetryPacket.objects.filter(launch = launch).order_by('-time_received')[0]
        return JsonResponse(latest_packet.telemetry)
    except LaunchInfo.DoesNotExist:
        return Http404()

def index(req):
    ''' HI '''
    return HttpResponse("Welcome!")

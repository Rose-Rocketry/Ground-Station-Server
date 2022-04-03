from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import *

# Create your views here.
def get_all_launches(req):
    """Returns a json list of all items"""
    launches = LaunchInfo.objects.all()
    list = []
    for launch in launches:
        list.append({"name":str(launch), "id":str(launch.id), "active":str(launch.active_launch)})

    return JsonResponse({"launches": list})

@csrf_exempt
def send_telemetry(req, payload_id):
    '''Temporary Send Data'''
    if req.method != "POST":
        return HttpResponse("🎉 You should not be seeing this. XP")
    try:
        launch = LaunchInfo.objects.get(flight_computer=payload_id, active_launch=True)
        print(req.body)
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

def get_peripheral_launches(req, peripheral_id):
    '''
    Gets all ative launches that use the given peripheral id.
        The format is {launch name : launch id (id to be passed in url)}
    '''
    try:
        peripheral = PeripheralStatus.objects.get(p_id=peripheral_id)
        launches = peripheral.launch.all()

        launch_list = []
        for launch in launches:
            launch_list.append({"name":str(launch), "id": launch.id})
        return JsonResponse({"launches":launch_list})

    except PeripheralStatus.DoesNotExist:
        return Http404()
    

def index(req):
    ''' HI '''
    return HttpResponse("Welcome!")

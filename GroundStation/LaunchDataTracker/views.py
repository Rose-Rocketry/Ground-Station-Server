from django import views
from django.http import Http404, JsonResponse
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from .serializers import PayloadSerializer, PeripheralSerializer, UserSerializer, GroupSerializer, LaunchSerializer
from rest_framework import viewsets, permissions

from .models import *

# Create your views here.
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


### API Endpoints
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class LaunchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows launches to be viewed or edited.
    """
    queryset = LaunchInfo.objects.all()
    serializer_class = LaunchSerializer
    permission_classes = [permissions.AllowAny]

class PayloadViewSet(viewsets.ModelViewSet):
    """
    Gets all payloads
    """
    queryset = Payload.objects.all()
    serializer_class = PayloadSerializer
    permission_classes = [permissions.AllowAny]

class PeripheralViewSet(viewsets.ModelViewSet):
    """
    Gets all peripherals
    """
    queryset = PeripheralStatus.objects.all()
    serializer_class = PeripheralSerializer
    permission_classes = [permissions.AllowAny]
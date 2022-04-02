
from .models import *
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async


class TelemetryConsumer(WebsocketConsumer):
    """This is the consumer for the telemetry"""
        

    def connect(self):
        """Handle when a new connection is being made"""
        self.payload = self.scope['url_route']['kwargs']['payload_name']
        async_to_sync(self.channel_layer.group_add)("telemetry", self.channel_name)

        try:
            #Payload and launches
            payload = Payload.objects.get(model_name = self.payload)
            self.launch = LaunchInfo.objects.get(flight_computer = payload, active_launch=True)
            self.accept()
            return
        except LaunchInfo.DoesNotExist:
            print("Failed to get launch info")
            self.accept()
            self.send("{\"status\":\"No Launch Info\"")
            self.close()
            return

    

    def disconnect(self, code):
        """Handle when the socket is disconnected."""
        async_to_sync(self.channel_layer.group_discard)(self.payload, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        """Handle when data is received."""
        #print(f"Received Data: {text_data} {bytes_data}")
        try:
            data = json.loads(text_data)

            #Send Messages to all clients:
            async_to_sync(self.channel_layer.group_send)(
                self.payload,
                {
                    "type": "telemetry_message",
                    "data": data
                }
            )

            TelemetryPacket.objects.create(telemetry = data, launch = self.launch)
            
        except ValueError:
            print(f"Invalid data from payload: {self.payload}")

    def telemetry_message(self, event):
        """Prints the event"""
        #print(event)
        

class ClientConsumer(WebsocketConsumer):
    """This pipes data to the client consumer."""
    
    def connect(self):
        """Handles when socket is connected"""
        async_to_sync(self.channel_layer.group_add)("telemetry", self.channel_name)
        self.accept()

        #TODO get all connected peripherals for the given launch

    def disconnect(self, code):
        """Handle when the socket is disconnected."""
        #TODO Send a message of things connected and disconnected
        async_to_sync(self.channel_layer.group_discard)(self.payload, self.channel_name)
        

    def receive(self, text_data=None, bytes_data=None):
        """Handle when data is received."""
        

    def telemetry_message(self, event):
        """A handler for receiving telemetry"""
        self.send(json.dumps(event["data"]))

    def status_message(self, event):
        """Handles application level"""


        
class PeripheralConsumer(WebsocketConsumer):
    """A consumer for communication between the GS and a peripheral."""

    def connect(self):
        self.peripheral = self.scope['url_route']['kwargs']['peripheral_name']
        #Sender should be the device.
        self.sender = self.scope['url_route']['kwargs']['sender_name']
        async_to_sync(self.channel_layer.group_add)(self.peripheral, self.channel_name)
        
        #Get database objects
        peripherals = PeripheralStatus.objects.filter(p_id = self.peripheral)
        if len(peripherals) == 0:
            peripherals = PeripheralStatus.objects.create(p_id=self.peripheral)

        if len(peripherals[0].launch.filter(active_launch=True)) == 0:
            self.accept()
            self.send(json.dumps({"status":"failed", "reason":"No launch found."}))
            self.close()
            return

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_disconnect)(self.peripheral, self.channel_name)

    def state_update(self, event):
        """Handles when the state of the device is updated"""
        
        if event['sender'] != self.sender:
            self.send(json.dumps(event["data"]))

    def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)

            #Send Messages to all clients:
            async_to_sync(self.channel_layer.group_send)(
                self.peripheral,
                {
                    "type": "state_update",
                    "sender":self.sender,
                    "data": data
                }
            )

        except ValueError:
            print(f"Invalid status for {self.peripheral}")
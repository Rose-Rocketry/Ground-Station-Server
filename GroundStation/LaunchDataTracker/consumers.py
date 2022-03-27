
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
        async_to_sync(self.channel_layer.group_add)(self.payload, self.channel_name)

        try:
            #Payload and launches
            payload = Payload.objects.get(model_name = self.payload)
            self.launch = LaunchInfo.objects.get(flight_computer = payload, active_launch=True)
            self.accept()
        except LaunchInfo.DoesNotExist:
            print("Failed to get launch info")
            self.accept()
            self.send("{\"status\":\"No Launch Info\"")
            self.close()

    

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
        

class ClientTelemetryConsumer(WebsocketConsumer):
    """This pipes data to the client consumer."""
    
    def connect(self):
        """Handles when socket is connected"""
        self.payload = self.scope['url_route']['kwargs']['payload_name']
        async_to_sync(self.channel_layer.group_add)(self.payload, self.channel_name)
        """Handle when a new connection is being made"""
        self.accept()

    def disconnect(self, code):
        """Handle when the socket is disconnected."""
        
        async_to_sync(self.channel_layer.group_discard)(self.payload, self.channel_name)
        

    def receive(self, text_data=None, bytes_data=None):
        """Handle when data is received."""
        

    def telemetry_message(self, event):
        """A handler for receiving telemetry"""
        self.send(json.dumps(event))
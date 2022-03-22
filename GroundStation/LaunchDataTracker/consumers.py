import json
from channels.generic.websocket import WebsocketConsumer

class TelemetryConsumer(WebsocketConsumer):
    """This is the consumer for the telemetry"""

    def connect(self):
        """Handle when a new connection is being made"""
        self.accept()

    def disconnect(self, code):
        """Handle when the socket is disconnected."""
        pass

    def receive(self, text_data=None, bytes_data=None):
        """Handle when data is received."""
        pass

class ClientTelemetryConsumer(WebsocketConsumer):
    """This pipes data to the client consumer."""
    
    def connect(self):
        """Handle when a new connection is being made"""
        self.accept()

    def disconnect(self, code):
        """Handle when the socket is disconnected."""
        pass

    def receive(self, text_data=None, bytes_data=None):
        """Handle when data is received."""
        pass
from django.db import models
# Create your models here.


class LaunchInfo(models.Model):
    '''A model for a launch at a given site.'''
    liftoff_time = models.DateTimeField("Est. Liftoff Time")
    active_launch = models.BooleanField("Launch Active")
    flight_computer = models.CharField("Payload ID", max_length=255)

    def __str__(self):
        return str(self.liftoff_time) + (":ACTIVE " if self.active_launch else ":INACTIVE ")+ self.flight_computer

class TelemetryPacket(models.Model):
    '''A model for recording the packets sent from any rocket.'''
    def _default_packet(self):
        return {"status":"invalid"}

    time_received = models.DateTimeField("Time Received",auto_now_add=True)
    telemetry = models.JSONField("Raw Telemetry", default = _default_packet)
    launch = models.ForeignKey(LaunchInfo, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.time_received)+" "+str(self.telemetry)+" "+self.launch.flight_computer

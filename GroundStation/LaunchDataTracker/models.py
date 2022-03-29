from django.db import models
# Create your models here.

class Payload(models.Model):
    """Return default features"""
    def _default_features():
        """Get default features"""
        return {'features': ['minimum']}

    model_name = models.CharField("Payload ID", max_length=255, unique=True)
    features = models.JSONField("Feature Set", default = _default_features)

    def __str__(self):
        return self.model_name.__str__()

class LaunchInfo(models.Model):
    """ Information about the launch parameters """
    class Meta:
        """ Meta information about launch parameters """
        constraints = [
            models.UniqueConstraint(fields=['flight_computer'], condition=models.Q(active_launch=True), name='unique_active_launch')
        ]

    liftoff_time = models.DateTimeField("Est. Liftoff Time")
    active_launch = models.BooleanField("Launch Active")
    flight_computer = models.ForeignKey(Payload, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.liftoff_time) + (":ACTIVE " if self.active_launch else ":INACTIVE ")+ self.flight_computer.model_name

class TelemetryPacket(models.Model):
    '''A model for recording the packets sent from any rocket.'''
    def _default_packet():
        return {"status":"invalid"}

    time_received = models.DateTimeField("Time Received",auto_now_add=True)
    telemetry = models.JSONField("Raw Telemetry", default = _default_packet)
    launch = models.ForeignKey(LaunchInfo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.time_received} {self.telemetry} {self.launch.flight_computer.model_name}"

class PeripheralStatus(models.Model):
    """ A database for the parameters and settings of a peripheral. """
    def _default_status():
        return {"status": "none"}
        
    launch = models.ManyToManyField(LaunchInfo)
    p_id = models.CharField("Peripheral ID", max_length=255, unique=True)
    p_data = models.JSONField("Data",default = _default_status )

    def __str__(self):
        return self.p_id.__str__()
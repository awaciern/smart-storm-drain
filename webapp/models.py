from django.db import models
from django.utils import timezone


class Device(models.Model):
    name = models.CharField(max_length=100)
    # location will be needed
    # Health status will be needed too???

    def __str__(self):
        return self.name


class Transmission(models.Model):
    LEVELS = (
        (0, 'None'),
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    )
    timestamp = models.DateTimeField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    depth = models.FloatField()
    flowrate = models.IntegerField(choices=LEVELS)
    voltage = models.FloatField()

    def __str__(self):
        return '{0} at {1}'.format(self.device, self.timestamp)

from django.db import models
from django.utils import timezone


# class Message(models.Model):
#     text = models.CharField(max_length=100)
#     date = models.DateTimeField(default=timezone.now)
#
#     def __str__(self):
#         return self.text


class Device(models.Model):
    name = models.CharField(max_length=100)
    # location will be needed

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

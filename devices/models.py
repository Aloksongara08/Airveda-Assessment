from django.db import models

class Device(models.Model):
    uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TemperatureReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="temperature_readings")
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)


class HumidityReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="humidity_readings")
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

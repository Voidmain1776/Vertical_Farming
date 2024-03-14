from django.db import models

# to create database schema

class SensorData(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    moisture = models.FloatField(null=True)
    lux = models.FloatField(null=True)
    phlevel = models.FloatField(null=True)

    def __str__(self):
        return f"Temp: {self.temperature}°C, Humidity: {self.humidity}%, Moisture: {self.moisture}, Lux: {self.lux}, pH: {self.phlevel}"




from django.db import models


class SensorData(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    water_level = models.FloatField(null=True, blank=True)
    rain = models.BooleanField(default=False)
    light = models.BooleanField(default=False)


class DailyStats(models.Model):
    date = models.DateField(unique=True)
    max_temperature = models.FloatField(null=True, blank=True)
    min_temperature = models.FloatField(null=True, blank=True)
    max_humidity = models.FloatField(null=True, blank=True)
    min_humidity = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Stats for {self.date}"
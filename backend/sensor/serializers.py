# import serializers from the REST framework
from rest_framework import serializers

# import the SensorData model
from .models import SensorData

# create a serializer class for SensorData
class SensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorData
        fields = ('id', 'temperature', 'humidity', 'water_level', 'rain', 'light')
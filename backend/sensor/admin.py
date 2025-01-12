from django.contrib import admin

# Import the SensorData model
from .models import SensorData

# Create a class for the admin-model integration
class SensorDataAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin panel
    list_display = ("temperature", "humidity", "water_level", "rain", "light")

# Register the SensorData model with the admin panel
admin.site.register(SensorData, SensorDataAdmin)
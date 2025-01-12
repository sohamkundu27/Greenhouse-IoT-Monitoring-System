from django.urls import path
from sensor.views import SensorDataListCreateView, DailyStatsView
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/sensors/', SensorDataListCreateView.as_view(), name='sensor-data-list-create'),
    path('api/daily-stats/', DailyStatsView.as_view(), name='daily-stats'),
]
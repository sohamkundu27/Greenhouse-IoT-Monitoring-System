from django.utils.timezone import now
from datetime import timedelta, datetime
from django.db.models import Max, Min
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData, DailyStats
from .serializers import SensorDataSerializer


class SensorDataListCreateView(APIView):
    def get(self, request):
        # Fetch all sensor data
        sensor_data = SensorData.objects.all()
        serializer = SensorDataSerializer(sensor_data, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Add new sensor data
        serializer = SensorDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailyStatsView(APIView):
    def get(self, request):
        try:
            # Define today's date range
            start_of_day = now().replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = start_of_day + timedelta(days=1)

            # Check if stats for today already exist in the database
            daily_stats, created = DailyStats.objects.get_or_create(date=start_of_day.date())

            if not created:
                # If the stats are already calculated, return them
                return Response({
                    "date": daily_stats.date,
                    "max_temperature": daily_stats.max_temperature,
                    "min_temperature": daily_stats.min_temperature,
                    "max_humidity": daily_stats.max_humidity,
                    "min_humidity": daily_stats.min_humidity,
                }, status=status.HTTP_200_OK)

            # Filter sensor data for today
            today_data = SensorData.objects.filter(created_at__gte=start_of_day, created_at__lt=end_of_day)

            if not today_data.exists():
                return Response(
                    {"message": "No data available for today."},
                    status=status.HTTP_200_OK
                )

            # Aggregate stats for today's data
            stats = today_data.aggregate(
                max_temperature=Max("temperature"),
                min_temperature=Min("temperature"),
                max_humidity=Max("humidity"),
                min_humidity=Min("humidity"),
            )

            # Save the aggregated stats in the database
            daily_stats.max_temperature = stats["max_temperature"]
            daily_stats.min_temperature = stats["min_temperature"]
            daily_stats.max_humidity = stats["max_humidity"]
            daily_stats.min_humidity = stats["min_humidity"]
            daily_stats.save()

            # Return the stats
            return Response({
                "date": daily_stats.date,
                "max_temperature": daily_stats.max_temperature,
                "min_temperature": daily_stats.min_temperature,
                "max_humidity": daily_stats.max_humidity,
                "min_humidity": daily_stats.min_humidity,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching daily stats.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MultiDayStatsView(APIView):
    def get(self, request):
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            if not start_date or not end_date:
                return Response({"error": "Start date and end date are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Parse dates
            try:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

            stats = DailyStats.objects.filter(date__range=[start_date, end_date]).order_by("date")
            serialized_stats = [
                {
                    "date": stat.date,
                    "max_temperature": stat.max_temperature,
                    "min_temperature": stat.min_temperature,
                    "max_humidity": stat.max_humidity,
                    "min_humidity": stat.min_humidity,
                }
                for stat in stats
            ]
            return Response(serialized_stats, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching stats.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
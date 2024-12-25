import adafruit_dht
import board
import time

# Initialize the DHT11 sensor
dht_device = adafruit_dht.DHT22(board.D4)  # GPIO 4 for DHT 11

while True:
    try:
        # Read temperature and humidity from the sensor
        temperature_c = dht_device.temperature  # Temperature in Celsius
        humidity = dht_device.humidity  # Humidity in percentage

        # Convert temperature to Fahrenheit
        temperature_f = temperature_c * 9 / 5 + 32

        # Print temperature in Fahrenheit and humidity
        print(f"Temp: {temperature_f:.1f}°F, Humidity: {humidity:.1f}%")
    except RuntimeError as error:
        # Handle intermittent errors
        print(f"Sensor error: {error.args[0]}")
    time.sleep(3)

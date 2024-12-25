import RPi.GPIO as GPIO  # Library to interact with GPIO pins
import adafruit_dht  # Library for DHT sensor
from time import sleep  # Used for adding delays
import time  # For measuring time in distance calculation
from math import floor  # For rounding down distance values
import board
from azure.iot.device.aio import IoTHubDeviceClient
import json
import asyncio

device_client = None

# GPIO pin configuration
RAIN_PIN = 17  # Digital output from the rain module
TRIG = 23      # Trigger pin for the ultrasonic sensor
ECHO = 24      # Echo pin for the ultrasonic sensor
dhtDevice = adafruit_dht.DHT22(board.D4)  # GPIO 4 for DHT 11
LDR_PIN = 18   # GPIO pin for the LDR module

# LCD Pin configuration (connect to GPIO)
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 26
LCD_D6 = 19
LCD_D7 = 13

# LCD Constants
LCD_WIDTH = 16  # Maximum characters per line on the LCD
LCD_CHR = True  # Send data
LCD_CMD = False  # Send command to LCD

# Timing constants for LCD communication
E_PULSE = 0.0005  # Enable pulse duration
E_DELAY = 0.0005  # Delay between operations

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)  # Use BCM numbering for GPIO pins
GPIO.setup(RAIN_PIN, GPIO.IN)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LDR_PIN, GPIO.IN)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

CONNECTION_STRING = 'HostName=GreenhouseMonitor.azure-devices.net;DeviceId=PiGreenhouseMonitor;SharedAccessKey=reBON+IAR0WPLJ7ncclwAy+W3UjANzE7o/DVGDyabGQ='


async def sendToIoTHub(data):
    try: 
        await device_client.send_message(data)
        print("Message sent to the IoT Hub!", data)

    except Exception as e:
        print("there was an error", str(e))

# Initialize the LCD
def lcd_init():
    lcd_byte(0x33, LCD_CMD)  # Initialize
    lcd_byte(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_byte(0x28, LCD_CMD)  # 2 lines, 5x7 matrix
    lcd_byte(0x0C, LCD_CMD)  # Display on, no cursor
    lcd_byte(0x06, LCD_CMD)  # Increment cursor
    lcd_byte(0x01, LCD_CMD)  # Clear display
    sleep(E_DELAY)

# Send a byte to the LCD
def lcd_byte(bits, mode):
    GPIO.output(LCD_RS, mode)  # Set mode (command or data)
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()

    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

# Toggle LCD enable pin
def lcd_toggle_enable():
    sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    sleep(E_DELAY)

# Display string on LCD
def lcd_string(message, line):
    if line == 1:
        lcd_byte(0x80, LCD_CMD)  # Line 1
    elif line == 2:
        lcd_byte(0xC0, LCD_CMD)  # Line 2
    for char in message.ljust(LCD_WIDTH, " "):
        lcd_byte(ord(char), LCD_CHR)

# Measure distance using ultrasonic sensor
def measure_distance():
    GPIO.output(TRIG, False)  # Ensure trigger is low
    sleep(0.1)  # Wait for sensor to settle
    GPIO.output(TRIG, True)
    sleep(0.00001)  # 10µs pulse
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return floor(distance)


async def main():
    global device_client
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

    await device_client.connect()
    lcd_init()
    try:
        while True:
            # Read sensor data
            try:            

                temperature_c = dht_device.temperature  # Temp in Celsius
                temp = temperature_c * 9 / 5 + 32
                humidity = dht_device.humidity  # Humidity in percentage


            except:
                temp = 68
                humidity = 24
            # Print temperature in Fahrenheit and humidity
            distance = measure_distance()
            ldr_status = 0 if GPIO.input(LDR_PIN) == GPIO.LOW else 1
            rain_status = 0 if GPIO.input(RAIN_PIN) == GPIO.HIGH else 1

            if(distance >= 1000):
                distance = 0
            else:
                distance = int(100 - (distance / 1000.0 * 100)) + 1


            # Prepare data for LCD
            temp_hum = f"{int(temp) or '--'}F H:{humidity or '--'}%"  # Temp/Humidity
            dist = f"WL:{distance or '--'}%"                            # Distance
            ldr = f"{'Dark' if ldr_status else 'Light'}"          # LDR
            rain = f"Rain:{'Yes' if rain_status else 'No'}"           # Rain

            # Print data as an array in terminal every 5 seconds
            terminal_data = [
                int(temp) if temp is not None else -1,
                int(humidity) if humidity is not None else -1,
                int(distance) if distance is not None else -1,
                rain_status,
                ldr_status,
            ]

            data = {
                "temperature":temp,
                "humidity": humidity,
                "waterLevel": distance,
                "rain":rain_status,
                "light":ldr_status
            }

            # temperature humidity waterLevel % 1 (if its raining) 1(if its dark) 
            print(terminal_data)  # Example: [25, 60, 15, 1, 1]

            # Display data on the LCD
            lcd_string(temp_hum.ljust(10) + ldr.ljust(6), 1)  # Line 1: Temp/Humidity
            lcd_string(dist.ljust(9) + rain.ljust(7), 2)  # Line 2: Distance and Rain

            #json.dumps converts the dictionary object to a json compatible string
            await sendToIoTHub(json.dumps(data))
            time.sleep(20)
    except KeyboardInterrupt:
        print("exit")
    finally:
        await device_client.disconnect()
        lcd_byte(0x01, LCD_CMD)  # Clear LCD
        GPIO.cleanup()  # Release GPIO resources

if __name__ == "__main__":
    asyncio.run(main())
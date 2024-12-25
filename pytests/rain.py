import RPi.GPIO as GPIO
import time

# GPIO pin configuration
RAIN_PIN = 17  # Digital output from the rain module (DO)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(RAIN_PIN, GPIO.IN)

print("Rain sensor test in progress...")
try:
    while True:
        if GPIO.input(RAIN_PIN) == GPIO.LOW:
            print("Rain detected!")
        else:
            print("No rain detected.")
        time.sleep(1)  # Check every second
except KeyboardInterrupt:
    print("Exiting program.")
    GPIO.cleanup()

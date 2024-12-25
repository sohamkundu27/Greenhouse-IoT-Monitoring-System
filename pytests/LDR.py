import RPi.GPIO as GPIO
import time

# Setup GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)  # Changed to GPIO 18, remove pull_up_down setting

print("Testing LDR module on GPIO 18...")
while True:
    ldr_value = GPIO.input(18)  # Read the LDR state
    print(f"LDR Output: {ldr_value}")  # Print raw HIGH/LOW value
    time.sleep(1)

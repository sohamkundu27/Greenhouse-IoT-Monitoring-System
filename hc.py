import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
GPIO.setwarnings(False)

TRIG = 23  # GPIO pin for Trigger
ECHO = 24  # GPIO pin for Echo

print("Distance Measurement In Progress")

# Set up the GPIO pins
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
print("Waiting For Sensor To Settle")

try:
    while True:
        GPIO.output(TRIG, False)
        time.sleep(2)

        # Send a pulse to the trigger pin
        GPIO.output(TRIG, True)
        time.sleep(0.00001)  # 10µs pulse
        GPIO.output(TRIG, False)

        # Measure the time for the echo response
        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start  # Calculate the pulse duration
        distance = pulse_duration * 17150  # Calculate distance (cm)
        distance = round(distance, 2)  # Round to 2 decimal places

        print("Distance:", distance, "cm")

        time.sleep(0.1)  # Wait 1 second before measuring again

except KeyboardInterrupt:
    print("Stopping distance measurement")
    GPIO.cleanup()  # Clean up GPIO settings

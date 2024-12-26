#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define TRIG 4 // WiringPi pin 4 (GPIO 23)
#define ECHO 5 // WiringPi pin 5 (GPIO 24)

void setup()
{
    wiringPiSetup();       // Initialize WiringPi library
    pinMode(TRIG, OUTPUT); // Set TRIG as output
    pinMode(ECHO, INPUT);  // Set ECHO as input

    // Ensure TRIG is low at startup
    digitalWrite(TRIG, LOW);
    delay(30); // Wait for sensor to settle
}

double measureDistance()
{
    // Send a 10-microsecond pulse to TRIG
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    // Wait for ECHO to go HIGH
    while (digitalRead(ECHO) == LOW)
        ;

    // Record the start time
    long startTime = micros();

    // Wait for ECHO to go LOW
    while (digitalRead(ECHO) == HIGH)
        ;

    // Record the end time
    long endTime = micros();

    // Calculate the distance in cm
    double duration = endTime - startTime;
    double distance = (duration / 2.0) * 0.0343; // Speed of sound: 343 m/s

    return distance;
}

int main()
{
    setup();

    printf("Ultrasonic Distance Sensor Initialized\n");

    while (1)
    {
        double distance = measureDistance();
        printf("Distance: %.2f cm\n", distance);

        delay(1000); // Wait 1 second before next measurement
    }

    return 0;
}

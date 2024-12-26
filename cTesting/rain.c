#include <wiringPi.h>
#include <stdio.h>

#define RAIN_SENSOR 6 // WiringPi pin 6 (GPIO 25)

void setup()
{
    wiringPiSetup();             // Initialize WiringPi library
    pinMode(RAIN_SENSOR, INPUT); // Set rain sensor pin as input
    printf("Rain Sensor Initialized\n");
}

void checkRain()
{
    int rainStatus = digitalRead(RAIN_SENSOR); // Read rain sensor status

    if (rainStatus == LOW)
    {
        printf("Rain Detected!\n");
    }
    else
    {
        printf("No Rain\n");
    }
}

int main()
{
    setup();

    while (1)
    {
        checkRain();
        delay(1000); // Check rain status every second
    }

    return 0;
}

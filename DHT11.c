#include <wiringPi.h>
#include <stdio.h>

#define LDR 1 // WiringPi pin 1 = GPIO 18 (BCM)

int main()
{
    if (wiringPiSetup() == -1)
    {
        printf("WiringPi setup failed. Exiting...\n");
        return 1;
    }

    pinMode(LDR, INPUT); // Set GPIO 18 as input

    while (1)
    {
        printf("LDR State: %d\n", digitalRead(LDR)); // Read the state of GPIO 18
        delay(500);                                  // 500ms delay
    }

    return 0;
}

#include <wiringPi.h>
#include <stdio.h>

// Define the GPIO pin for the LDR
#define LDR 1 // WiringPi pin 1 = GPIO 18 (BCM)

void test();

int main()
{
    // Initialize WiringPi
    if (wiringPiSetup() == -1)
    {
        printf("WiringPi setup failed. Exiting...\n");
        return 1;
    }

    // Run the test function in a loop
    while (1)
    {
        test();
        delay(500); // Add a small delay to avoid spamming the CPU
    }

    return 0;
}

void test()
{
    // Set pin to input mode
    pinMode(LDR, INPUT);

    // Read the digital state of the LDR pin
    int ldrValue = digitalRead(LDR);

    // Print the result
    if (ldrValue == HIGH)
    {
        printf("Light detected! LDR state: HIGH\n");
    }
    else
    {
        printf("Darkness detected! LDR state: LOW\n");
    }
}

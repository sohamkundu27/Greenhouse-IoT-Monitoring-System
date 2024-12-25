#include <wiringPi.h>
#include <stdio.h>

#define TEST_PIN 7

int main()
{
    if (wiringPiSetup() == -1)
    {
        printf("WiringPi setup failed!\n");
        return 1;
    }

    pinMode(TEST_PIN, OUTPUT);

    for (int i = 0; i < 100; i++)
    {
        digitalWrite(TEST_PIN, HIGH);
        printf("Pin HIGH\n");
        delay(50);
        digitalWrite(TEST_PIN, LOW);
        printf("Pin LOW\n");
        delay(50);
    }

    return 0;
}

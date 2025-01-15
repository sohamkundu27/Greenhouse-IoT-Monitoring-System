#include <wiringPi.h>
#include <stdio.h>

// GPIO pin configuration
#define DHT_PIN 4 // GPIO pin where DHT11 is connected (BCM numbering)

// Function declarations
int readDHT11Data(int *temperature, int *humidity);

int main()
{
    // Initialize WiringPi
    if (wiringPiSetupGpio() == -1)
    {
        printf("WiringPi setup failed. Exiting...\n");
        return 1;
    }

    int temperature = 0, humidity = 0;

    // Read and display DHT11 data
    while (1)
    {
        if (readDHT11Data(&temperature, &humidity))
        {
            printf("Temperature: %d°C, Humidity: %d%%\n", temperature, humidity);
        }
        else
        {
            printf("Failed to read from DHT11 sensor. Retrying...\n");
        }

        delay(2000); // Wait 2 seconds before the next reading
    }

    return 0;
}

// Function to read data from the DHT11 sensor
int readDHT11Data(int *temperature, int *humidity)
{
    uint8_t data[5] = {0, 0, 0, 0, 0}; // Buffer to store DHT11 data
    uint8_t lastState = HIGH;
    uint8_t counter = 0;
    uint8_t j = 0, i;

    // Signal the DHT11 to send data
    pinMode(DHT_PIN, OUTPUT);
    digitalWrite(DHT_PIN, LOW);
    delay(18); // 18 ms to start communication
    digitalWrite(DHT_PIN, HIGH);
    delayMicroseconds(40);
    pinMode(DHT_PIN, INPUT);

    // Read data from the DHT11 sensor
    for (i = 0; i < 85; i++)
    {
        counter = 0;
        while (digitalRead(DHT_PIN) == lastState)
        {
            counter++;
            delayMicroseconds(1);
            if (counter == 255)
                break;
        }

        lastState = digitalRead(DHT_PIN);

        if (counter == 255)
            break;

        // Ignore the first 3 transitions (initial response)
        if ((i >= 4) && (i % 2 == 0))
        {
            data[j / 8] <<= 1; // Shift to the left
            if (counter > 50)
                data[j / 8] |= 1;
            j++;
        }
    }

    // Validate the data
    if ((j >= 40) &&
        (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xFF)))
    {
        *humidity = data[0];
        *temperature = data[2];
        return 1; // Success
    }
    else
    {
        return 0; // Checksum failed
    }
}
#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <azureiot/iothub_client_core_common.h>
#include <azureiot/iothub_device_client_ll.h>
#include <azureiot/iothub_message.h>

#define TRIG 4        // GPIO 23
#define ECHO 5        // GPIO 24
#define RAIN_SENSOR 6 // GPIO 25
#define LDR_PIN 0     // Analog Pin (via MCP3008)

// Azure IoT Hub connection string
const char *connectionString = "HostName=GreenhouseMonitor.azure-devices.net;DeviceId=PiGreenhouseMonitor;SharedAccessKey=reBON+IAR0WPLJ7ncclwAy+W3UjANzE7o/DVGDyabGQ='";

// DHT11 Setup
#define MAX_TIMINGS 85
#define DHT_PIN 7
int dht_data[5] = {0, 0, 0, 0, 0};

// Function to read DHT11
int readDHT11(float *temperature, float *humidity)
{
    uint8_t laststate = HIGH;
    uint8_t counter = 0, j = 0;
    int i;
    dht_data[0] = dht_data[1] = dht_data[2] = dht_data[3] = dht_data[4] = 0;

    pinMode(DHT_PIN, OUTPUT);
    digitalWrite(DHT_PIN, LOW);
    delay(18);
    digitalWrite(DHT_PIN, HIGH);
    delayMicroseconds(40);
    pinMode(DHT_PIN, INPUT);

    for (i = 0; i < MAX_TIMINGS; i++)
    {
        counter = 0;
        while (digitalRead(DHT_PIN) == laststate)
        {
            counter++;
            delayMicroseconds(1);
            if (counter == 255)
                break;
        }
        laststate = digitalRead(DHT_PIN);

        if (counter == 255)
            break;

        if ((i >= 4) && (i % 2 == 0))
        {
            dht_data[j / 8] <<= 1;
            if (counter > 16)
                dht_data[j / 8] |= 1;
            j++;
        }
    }

    if ((j >= 40) && (dht_data[4] == ((dht_data[0] + dht_data[1] + dht_data[2] + dht_data[3]) & 0xFF)))
    {
        *humidity = dht_data[0];
        *temperature = dht_data[2];
        return 0;
    }
    else
    {
        return -1; // Error reading
    }
}

// Function to measure distance using HC-SR04
double measureDistance()
{
    digitalWrite(TRIG, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG, LOW);

    while (digitalRead(ECHO) == 0)
        ;
    long startTime = micros();

    while (digitalRead(ECHO) == 1)
        ;
    long endTime = micros();

    double distance = (endTime - startTime) * 0.0343 / 2;
    return distance;
}

// Azure IoT: Send data
void sendToAzure(float temperature, float humidity, double distance, int rain, int light)
{
    char message[256];
    snprintf(message, sizeof(message),
             "{\"temperature\": %.1f, \"humidity\": %.1f, \"distance\": %.2f, \"rain\": %d, \"light\": %d}",
             temperature, humidity, distance, rain, light);

    IOTHUB_MESSAGE_HANDLE messageHandle = IoTHubMessage_CreateFromString(message);
    if (messageHandle == NULL)
    {
        printf("Failed to create IoT Hub message\n");
        return;
    }

    IOTHUB_DEVICE_CLIENT_LL_HANDLE clientHandle = IoTHubDeviceClient_LL_CreateFromConnectionString(connectionString, MQTT_Protocol);
    if (clientHandle == NULL)
    {
        printf("Failed to create IoT Hub client\n");
        return;
    }

    IoTHubDeviceClient_LL_SendEventAsync(clientHandle, messageHandle, NULL, NULL);
    IoTHubMessage_Destroy(messageHandle);
    IoTHubDeviceClient_LL_DoWork(clientHandle);
    IoTHubDeviceClient_LL_Destroy(clientHandle);
}

int main()
{
    wiringPiSetup();
    pinMode(TRIG, OUTPUT);
    pinMode(ECHO, INPUT);
    pinMode(RAIN_SENSOR, INPUT);

    float temperature, humidity;
    double distance;
    int rain, light;

    while (1)
    {
        if (readDHT11(&temperature, &humidity) == -1)
        {
            printf("Failed to read DHT11\n");
        }

        distance = measureDistance();
        rain = digitalRead(RAIN_SENSOR) == LOW ? 1 : 0;

        // Read LDR (via MCP3008, simulated as random here)
        light = rand() % 1024; // Replace with actual ADC reading

        printf("Temp: %.1f°C, Humidity: %.1f%%, Distance: %.2fcm, Rain: %d, Light: %d\n",
               temperature, humidity, distance, rain, light);

        sendToAzure(temperature, humidity, distance, rain, light);
        delay(5000); // Send every 5 seconds
    }

    return 0;
}

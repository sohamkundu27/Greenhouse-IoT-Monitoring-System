import time
import json
import requests
from azure.eventhub import EventHubConsumerClient

# Replace with your Event Hub-compatible connection string and consumer group
CONNECTION_STRING = 'Endpoint=sb://iothub-ns-greenhouse-63572081-18b3f6e973.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=3N4v8qcq8hhxvxs4NCv5ZcXU6Q70o0lFrAIoTAy5MLg=;EntityPath=greenhousemonitor'
CONSUMER_GROUP = "$Default"
EVENTHUB_NAME = "greenhousemonitor"
DJANGO_API_URL = "http://localhost:8000/api/sensors/"  # Update to your sensor data endpoint

def send_to_django_api(data):
    """
    Sends the received event data to the Django API.
    """
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(DJANGO_API_URL, data=json.dumps(data), headers=headers)
        print(response)
        if response.status_code == 201:  # HTTP 201 Created
            print("Data successfully sent to Django API:", response.json())
        else:
            print(f"Failed to send data. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Error sending data to Django API: {str(e)}")

def on_event(partition_context, event):
    """
    Handles events received from the Event Hub.
    """
    try:
        # Parse the event data
        raw_data = json.loads(event.body_as_str()) # json string to python object
        print(f"Received raw event: {raw_data} from partition: {partition_context.partition_id}")

        # Map the incoming event data to match the SensorData fields
        data = {
            "temperature": raw_data.get("temperature"),
            "humidity": raw_data.get("humidity"),
            "water_level": raw_data.get("water_level"),
            "rain": raw_data.get("rain"),
            "light": raw_data.get("light"),
        }

        # Send the mapped data to Django API
        send_to_django_api(data)

        # Update the checkpoint to mark the event as processed
        partition_context.update_checkpoint(event)
    except Exception as e:
        print(f"Error processing event: {str(e)}")

def main():
    """
    Main function to listen for events and process them.
    """
    client = EventHubConsumerClient.from_connection_string(
        CONNECTION_STRING,
        consumer_group=CONSUMER_GROUP,
        eventhub_name=EVENTHUB_NAME,
    )
    try:
        print("Listening for the latest event...")
        with client:
            while True:
                client.receive(
                    on_event=on_event, #call back, not explicitly called. automatically called by client
                    starting_position="@latest",  # Only read the latest message
                )
                time.sleep(60)  # Wait for 1 minute before fetching the next message
    except KeyboardInterrupt:
        print("Stopped listening.")

if __name__ == "__main__":
    main()
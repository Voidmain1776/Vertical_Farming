import os
import django
import paho.mqtt.client as mqtt
import json
import random
# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartfarm.settings')  # Replace with your project's settings module
django.setup()

from backend.models import SensorData

# MQTT Broker Credentials
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = "omkar"
MQTT_PASSWORD = "omkar"

# MQTT Topics to Subscribe
MQTT_TOPIC_FARM_SENSOR = "farm/sensor"


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe([(MQTT_TOPIC_FARM_SENSOR, 0)])

def on_message(client, userdata, msg):
    payload_str = msg.payload.decode()
    try:
        payload = json.loads(payload_str)  # parse the payload
        # print(payload)
        # print(payload['temperature'], payload['humidity'])
    except ValueError:
        print(f"Invalid payload: {payload_str}")
        return

    

    if msg.topic == MQTT_TOPIC_FARM_SENSOR:
        try:
            random_moisture = round(random.uniform(400, 900), 1) # remove this after setting up sensor in esp32 
            random_lux=round(random.uniform(400, 800), 1)
            random_ph=round(random.uniform(0, 14), 1)
            sensor_data = SensorData.objects.create(temperature=payload['temperature'], humidity=payload['humidity'],moisture=random_moisture,lux=random_lux,phlevel=random_ph)
# sensor_data = SensorData.objects.create(temperature=payload['temperature'], humidity=payload['humidity'], moisture=payload['moisture'],lux=payload['lux'],phlevel=payload['phlevel'])

            print("Temperature data saved:", sensor_data)
        except Exception as e:
            print("Error saving temperature data:", e)

    else:
        print("Error saving humidity data:", e)


client = mqtt.Client()
client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
client.loop_forever()


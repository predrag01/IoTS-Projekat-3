import paho.mqtt.client as paho
import json
import time
from datetime import datetime, timedelta
from nats.aio.client import Client as NATS
import asyncio

sensor = "sensor/weather-data"
nats_topic = "nats-weather-data"

last_publish_time = time.time()
temperature_readings = []
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected with result code " + str(rc))
        client.subscribe(sensor + "/+")
        print("Subscribed to topic: " + sensor)
    else:
        print(f"Failed to connect to MQTT broker with result code {rc}")
def on_message(client, userdatqa, msg):
    try:
        if msg.topic.startswith(sensor):
            data = json.loads(msg.payload)
            print("Received message from mosquitto:")
            print(data)
            process_data(data)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Failed to deserialize message: {e}")

def on_publish(client, userdata, mid):
    print("Message published")

def process_data(data):
    global last_publish_time

    temperature = data.get("AirTemperature")

    if temperature is not None:
        temperature_readings.append(temperature)

    current_time = time.time()
    if current_time - last_publish_time >= 10:
        if temperature_readings:
            average_temp = sum(temperature_readings) / len(temperature_readings)
            print("Average air temperature in 10s:", average_temp)
            message = {
                "average_temperature": average_temp,
                "timestamp": datetime.utcnow().isoformat()
            }
            asyncio.run(publish_average_temp(message))
            temperature_readings.clear()
            last_publish_time = current_time

async def publish_average_temp(average_temp):
    try:
        nc = NATS()
        await nc.connect(servers=["nats://nats:4222"])
        await nc.publish(nats_topic, json.dumps(average_temp).encode('utf-8'))
        await nc.drain()
        print("Average temperature published to NATS:", average_temp)
    except Exception as e:
        print(f"Failed to publish data to NATS: {e}")


def start_analytics():
    client = paho.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect("mosquitto", 8883, 60)
    client.loop_forever()

if __name__ == "__main__":
    start_analytics()
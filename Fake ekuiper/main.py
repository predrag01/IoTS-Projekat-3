import paho.mqtt.client as paho
import json

sensor = "sensor/weather-data"
ekuiper = "ekuiper/weather-data"
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

            temperature = data.get("AirTemperature")

            if temperature is not None:
                message = {
                    "StationName": data.get("StationName"),
                    "MeasurementTimestamp": data.get("MeasurementTimestamp"),
                    "AirTemperature": data.get("AirTemperature")
                }
                if temperature > 30:
                    message["Warning"]="Temperature is too high!"
                    json_data = json.dumps(message)
                    print(f"Temperature is over 30C: {message}")
                    client.publish(ekuiper, payload=json_data, qos=1)
                elif temperature < 0:
                    message["Warning"] = "Temperature is too low!"
                    json_data = json.dumps(message)
                    print(f"Temperature is under 0C: {message}")
                    client.publish(ekuiper, payload=json_data, qos=1)

    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
        print(f"Failed to deserialize message: {e}")
def on_publish(client, userdata, mid):
    print("Message published")
def start_analytics():
    client = paho.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.connect("mosquitto", 8883, 60)
    client.loop_forever()

if __name__ == "__main__":
    start_analytics()
import asyncio
import json
from nats.aio.client import Client as NATS
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

nats_topic = "nats-weather-data"

influxdb = "http://influxdb:8086"
influx_token = "Uc6NSyoBSKeojYZjLRHqllXJ7Be-mhRlS8ueXbKbCbVBJ9N2S_qigrONMkMmRWQVqtFus9l10q64mDFg4eZdpA=="
influx_org = "weather.org"
influx_bucket = "weather_data"
async def subscribeToNats():
    try:
        nc = NATS()
        await nc.connect(servers=["nats://nats:4222"])

        client = InfluxDBClient(url=influxdb, token=influx_token, org=influx_org)
        write_api = client.write_api(write_options=SYNCHRONOUS)

        async def message_handler(msg):
            nonlocal write_api
            payload = msg.data.decode()
            try:
                data = json.loads(payload)

                point = Point("weather_data") \
                    .field("average_temperature", data["average_temperature"]) \
                    .time(data["timestamp"])

                write_api.write(influx_bucket, influx_org, point)
                print(f"Stored data in InfluxDB: {data}")

            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")
            except Exception as e:
                print(f"Error storing data in InfluxDB: {e}")

        await nc.subscribe(nats_topic, cb=message_handler)

        print(f"Subscribed to NATS topic '{nats_topic}'")

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error subscribing to NATS or storing data: {e}")

if __name__ == '__main__':
    asyncio.run(subscribeToNats())

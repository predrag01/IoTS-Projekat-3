import asyncio
import json
from nats.aio.client import Client as NATS

nats_topic = "nats-weather-data"
async def subscribeToNats():
    try:
        nc = NATS()
        await nc.connect(servers=["nats://localhost:4222"])

        async def message_handler(msg):
            payload = msg.data.decode()
            try:
                data = json.loads(payload)

                print(f"Received a message on: {data}")
            except json.JSONDecodeError as e:
                print(f"Failed to decode JSON: {e}")

        await nc.subscribe(nats_topic, cb=message_handler)

        print(f"Subscribed to NATS topic '{nats_topic}'")

        while True:
            await asyncio.sleep(1)

    except Exception as e:
        print(f"Error subscribing to NATS or storing data: {e}")

if __name__ == '__main__':
    asyncio.run(subscribeToNats())

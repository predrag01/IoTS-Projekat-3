import asyncio
from nats.aio.client import Client as NATS

nats_topic = "nats-weather-data"

async def run():
    nc = NATS()

    async def message_handler(msg):
        data = msg.data.decode('utf-8')
        print(f"Received a message on '{msg.subject}': {data}")

    try:
        await nc.connect(servers=["nats://nats:4222"])
        print("Connected to NATS server.")

        await nc.subscribe(nats_topic, cb=message_handler)
        print("Subscribed to 'nats-weather-data' topic. Waiting for messages...")

        # Keep the script running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        await nc.drain()

if __name__ == '__main__':
    asyncio.run(run())

FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install nats-py numpy aiohttp influxdb-client

CMD ["python", "main.py"]

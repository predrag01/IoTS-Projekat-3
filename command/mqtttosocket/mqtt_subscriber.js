const mqtt = require('mqtt');
const WebSocket = require('ws');

const brokerUrl = 'mqtt://mosquitto:8883';
const topic = 'ekuiper/weather-data';

const mqttClient = mqtt.connect(brokerUrl);

const wss = new WebSocket.Server({ port: 8080 });

mqttClient.on('connect', () => {
  console.log('Connected to MQTT broker');
  mqttClient.subscribe(topic, (err) => {
    if (!err) {
      console.log(`Subscribed to topic: ${topic}`);
    } else {
      console.error(`Failed to subscribe to topic: ${err.message}`);
    }
  });
});

mqttClient.on('message', (topic, message) => {
  console.log(`Received message on topic ${topic}: ${message.toString()}`);
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(message.toString());
    }
  });
});

mqttClient.on('error', (err) => {
  console.error(`Connection error: ${err.message}`);
});

wss.on('connection', (ws) => {
  console.log('WebSocket client connected');
  ws.on('close', () => {
    console.log('WebSocket client disconnected');
  });
});

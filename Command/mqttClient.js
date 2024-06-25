const mqtt = require('mqtt');

const brokerUrl = 'mqtt://mosquitto:8883'
const topic = ('ekuiper/weather-data')

const client = mqtt.connect(brokerUrl)

client.on('connect', () => {
    console.log('Connected to MQTT broker')
    client.subscribe(topic, (err) => {
        if (!err) {
            console.log(`Subscribed to topic: ${topic}`)
        } else {
            console.error(`Failed to subscribe to topic: ${err.message}`)
        }
    })
})

client.on('message', (topic, message) => {
    console.log(`Received message on topic ${topic}: ${message.toString()}`)
})

client.on('error', (err) => {
    console.error(`Connection error: ${err.message}`)
})

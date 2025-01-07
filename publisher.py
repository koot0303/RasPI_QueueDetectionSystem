import paho.mqtt.client as mqtt
import random
import json

broker = "test.mosquitto.org"
port = 1883
topic = "test/test"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
client.connect(broker, port)

data = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
    }
message = json.dumps(data)
client.publish(topic, message)
client.disconnect()

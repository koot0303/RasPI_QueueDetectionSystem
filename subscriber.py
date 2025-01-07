import paho.mqtt.client as mqtt
import random
import json

broker = "test.mosquitto.org"
port = 1883
topic = "test/test"

def on_message(client, userdata, message):
    data = json.loads(message.payload.decode('utf-8'))
    print(f"Received message: {data}")


client_id = f'python-mqtt-{random.randint(0, 1000)}'
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id)
client.connect(broker, port)
client.subscribe(topic)
client.on_message = on_message

client.loop_forever()

import paho.mqtt.client as mqtt

broker = "ブローカーのIPアドレス"
port = 1883
topic = "test/topic"

def on_message(client, userdata, message):
    print(f"Received message: {message.payload.decode('utf-8')}")

client = mqtt.Client()
client.connect(broker, port)
client.subscribe(topic)
client.on_message = on_message

client.loop_forever()

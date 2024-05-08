import uuid
import paho.mqtt.client as mqtt
import time
import json

# This is an example client for retrieving AIS data from the Digitraffic API
# https://www.digitraffic.fi/en/marine-traffic/

APP_NAME = 'Test/TestApp'
TOPIC = 'vessels-v2/#'

#########
def format_message(message):
    topic_hierarchy = str(message.topic).split("/")
    print(topic_hierarchy)
    id = topic_hierarchy[1]
    topic = topic_hierarchy[2]
    payload = message.payload.decode('utf-8')
    return id, topic, payload
    
def on_message(client, userdata, message):
    id, topic, payload = format_message(message)
    print("MMSI : " + id)
    print("Topic : " + topic)
    print("Payload : " + payload)
    print("----")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected')
        client.subscribe(TOPIC)
        print("Subscribing to topic:", TOPIC)
    else:
        print('Failed to connect, return code %d\n', rc)

client_name = '{}; {}'.format(APP_NAME, str(uuid.uuid4()))
client = mqtt.Client(client_name, transport="websockets")

client.on_connect = on_connect
client.on_message = on_message

client.tls_set()
client.connect('meri.digitraffic.fi', 443)

client.loop_start()
time.sleep(10)
client.loop_stop()
client.disconnect()

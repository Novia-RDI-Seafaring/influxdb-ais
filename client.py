import uuid
import paho.mqtt.client as mqtt
import time

# This is an example client for retrieving AIS data from the Digitraffic API
# https://www.digitraffic.fi/en/marine-traffic/

APP_NAME = 'Test/TestApp'
TOPIC = 'vessels-v2/#'

#########

def on_message(client, userdata, message):
    print('Topic:', str(message.topic))
    print('Payload:',  str(message.payload.decode('utf-8')))
    print('----')

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
time.sleep(60)
client.loop_stop()
client.disconnect()
import uuid
import paho.mqtt.client as mqtt
import time
import json
import influxdb_client, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# This is an example client for retrieving AIS data from the Digitraffic API
# https://www.digitraffic.fi/en/marine-traffic/

APP_NAME = 'Test/TestApp'
TOPIC = 'vessels-v2/#'

######## influxdb #########
BUCKET = "digitraffic-ais"
SENSOR = "digitraffic-ais"

#laod credentials
with open('credentials.json') as json_file:
  credentials = json.load(json_file)
  PORT = 8086
  TOKEN = str(credentials["token"])
  ORG = credentials["org"]
  HOST = credentials["host"]

#### utils #####
def write_data(message,bucket,sensor_name):
    '''Writes data to influxdb bucket'''
    topic_hierarchy = str(message.topic).split("/")
    #check if
    if len(topic_hierarchy)>2:
        #convert string to dict
        payload = json.loads(message.payload.decode('utf-8'))
        id = topic_hierarchy[1]
        topic = topic_hierarchy[2]
        #print(id,topic)

        #loop over points in payload
        for key, value in payload.items():
            if key == 'time':
                key = 'timepoint'
            point = (
                Point(sensor_name).tag(id,topic).field(key,value)
            )
            influx_write_api.write(bucket=bucket, org="Home", record=point)
   
def on_message(client, userdata, message):
    write_data(message,BUCKET,SENSOR)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected')
        client.subscribe(TOPIC)
        print("Subscribing to topic:", TOPIC)
    else:
        print('Failed to connect, return code %d\n', rc)

#create client
influx_client = influxdb_client.InfluxDBClient(url=HOST, token=TOKEN, org=ORG)
influx_write_api = influx_client.write_api(write_options=SYNCHRONOUS)

######## Digitraffic api client ########
DIGITRAFFIC_HOST = 'meri.digitraffic.fi'
DIGITRAFFIC_PORT = 443

#client
digitraffic_client_name = '{}; {}'.format(APP_NAME, str(uuid.uuid4()))
digitraffic_client = mqtt.Client(digitraffic_client_name, transport="websockets")

#callbacks
digitraffic_client.on_connect = on_connect
digitraffic_client.on_message = on_message
digitraffic_client.tls_set()

#### Connect to Digitraffic API ####
digitraffic_client.connect(DIGITRAFFIC_HOST, DIGITRAFFIC_PORT)

digitraffic_client.loop_start()

if __name__ == "__main__":
    digitraffic_client.loop_start()
    while True:
        time.sleep(1)

#time.sleep(60*10)
#digitraffic_client.loop_stop()
#digitraffic_client.disconnect()

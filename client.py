import uuid
import dotenv, os
import paho.mqtt.client as mqtt
import time
import json
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# This is an example client for retrieving AIS data from the Digitraffic API
# https://www.digitraffic.fi/en/marine-traffic/

APP_NAME = 'Test/TestApp'
TOPIC = 'vessels-v2/#'

######## influxdb #########
BUCKET = "digitraffic-api"
SENSOR = "ais"

#load environment variables
dotenv.load_dotenv('.env')
PORT = os.environ["INFLUX_PORT"]
TOKEN = os.environ["INFLUX_TOKEN"]
ORG = os.environ["INFLUX_ORG"]
HOST = os.environ["INFLUX_HOST"]

#### utils #####
def write_data(message,org,bucket,sensor):
    '''Writes data to influxdb bucket'''
    topics = str(message.topic).split("/")
    if len(topics)>2:
        tags = {
            "mmsi": topics[1],
            "type": topics[2]
        }
        payload = json.loads(message.payload.decode('utf-8'))
        point = Point(sensor)
        point.time(time.time_ns())
        # add tags
        for key, value in tags.items():
            point.tag(key,value)
        # add fields
        for key, value in payload.items():
            point.field(key,value)
        # write to db
        influx_write_api.write(bucket=bucket, org=org, record=point)
   
def on_message(client, userdata, message):
    write_data(message,ORG,BUCKET,SENSOR)

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

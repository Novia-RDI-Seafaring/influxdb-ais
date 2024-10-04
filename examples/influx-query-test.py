import uuid
import dotenv, os
import paho.mqtt.client as mqtt
import time
import json
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

APP_NAME = 'Test/TestApp'
TOPIC = 'vessels-v2/#'

######## influxdb #########
BUCKET = "digitraffic-ais"
SENSOR = "digitraffic-ais"

#load environment variables
dotenv.load_dotenv('.env')
PORT = os.environ["INFLUX_PORT"]
TOKEN = os.environ["INFLUX_TOKEN"]
ORG = os.environ["INFLUX_ORG"]
HOST = os.environ["INFLUX_HOST"]

#create client
influx_client = influxdb_client.InfluxDBClient(url=HOST, token=TOKEN, org=ORG)

query_api = influx_client.query_api()

query = f"""from(bucket: "{BUCKET}")
 |> range(start: -1m)
 |> filter(fn: (r) => r._measurement == "{SENSOR}")
 """
tables = query_api.query(query, org=ORG)

for table in tables:
   for record in table.records:
     print(record)

import uuid
import paho.mqtt.client as mqtt
import time
import json
import influxdb_client, os
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

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

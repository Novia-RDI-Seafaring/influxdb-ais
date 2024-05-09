import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json


credentials = json.load(open('credentials.json'))
PORT = 8086
TOKEN = str(credentials["token"])
ORG = credentials["org"]
HOST = credentials["host"]

write_client = influxdb_client.InfluxDBClient(url=HOST, token=TOKEN, org=ORG)

#
bucket="test-bucket"
write_api = write_client.write_api(write_options=SYNCHRONOUS)
   
for value in range(10):
  print(value)
  point = (
    Point("measurement1")
    .tag("tagname1", "test")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="Home", record=point)
  time.sleep(1) # separate points by 1 second


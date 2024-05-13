import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

with open('credentials.json') as json_file:
  credentials = json.load(json_file)
  PORT = 8086
  TOKEN = str(credentials["token"])
  ORG = credentials["org"]
  HOST = credentials["host"]

write_client = influxdb_client.InfluxDBClient(url=HOST, token=TOKEN, org=ORG)

#
bucket="ais-test"
write_api = write_client.write_api(write_options=SYNCHRONOUS)

ais = {
  "mmsi" : 273357260,
  "sog" : 9.7,
  "cog" : 216.6,
  "navStat" : 0,
  "rot" : 3,
  "posAcc" : True,
  "raim" : False,
  "heading" : 220,
  "timestamp" : 32,
  "timestampExternal" : 1659950974701
}

for key, value in ais.items():
  point = (
    Point("ais").tag("mmsi",ais["mmsi"]).field(key,value)
  )
  write_api.write(bucket=bucket, org="Home", record=point)


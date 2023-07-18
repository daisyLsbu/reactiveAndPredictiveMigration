import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#writing data to db
write_api = client.write_api(write_options=SYNCHRONOUS)
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="LSBU", record=point)
  time.sleep(1) # separate points by 1 second

#querying data from db
query_api = client.query_api()

query = """from(bucket: "telemetryData")
 |> range(start: -10m)
 |> filter(fn: (r) => r._measurement == "measurement1")"""
tables = query_api.query(query, org="LSBU")

for table in tables:
  for record in table.records:
    print(record)

#querying aggregated data from db
query_api = client.query_api()

query = """from(bucket: "telemetryData")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")
  |> mean()"""
tables = query_api.query(query, org="LSBU")

for table in tables:
    for record in table.records:
        print(record)


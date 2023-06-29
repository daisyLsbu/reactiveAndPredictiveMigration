import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#connect to influx db

#token = os.environ.get("INFLUXDB_TOKEN")
#token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
testBucketToken = "k0ow1rF9khxIMtElYfajigZYqKMAjr5-ydhcOgiUnExmiXWChMhUIAbXeOtTWA2DNR0d1jQfMpoTny25pCUrFQ=="
print(testBucketToken)

org = "LSBU"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url, token=testBucketToken, org=org)

bucket="test"
write_api = client.write_api(write_options=SYNCHRONOUS)

write_api.write(bucket=bucket, org="LSBU", record=point)



''''
#connect to bucket
bucket="telemetryData"

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
'''



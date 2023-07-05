import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#connect to bucket
bucket="telemetryData"

#connect to influx db
def connectToDB():
  #token = os.environ.get("INFLUXDB_TOKEN")
  token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  #testBucketToken = "k0ow1rF9khxIMtElYfajigZYqKMAjr5-ydhcOgiUnExmiXWChMhUIAbXeOtTWA2DNR0d1jQfMpoTny25pCUrFQ=="
  org = "LSBU"
  url = "http://localhost:8086"
  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def writeToDB(client, bucket):   
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

def readFromDB(client): 
  #querying data from db
  query_api = client.query_api()  
  query = """from(bucket: "telemetryData")
  |> range(start: -10m)
  |> filter(fn: (r) => r._measurement == "measurement1")"""
  tables = query_api.query(query, org="LSBU")

  for table in tables:
    for record in table.records:
      print(record)

def readAggFromDB(client):  
  #querying data from db
  query_api = client.query_api() 
  query = """from(bucket: "telemetryData")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "measurement1")
   |> mean()"""
  tables = query_api.query(query, org="LSBU")

  for table in tables:
      for record in table.records:
        print(record)

def writeToDB():
  write_api = client.write_api(write_options=SYNCHRONOUS)

  for value in range(5):
    point = (
      Point("test1")
      .tag("host", "10.0.0.9")
      .field("cpu", 45)
    )
    write_api.write(bucket=bucket, org="LSBU", record=point)
    time.sleep(1) # separate points by 1 second



client = connectToDB()
writeToDB(client, bucket)
writeToDB()

readFromDB(client)
readAggFromDB(client)

"""""
#connect to influx db

#token = os.environ.get("INFLUXDB_TOKEN")
token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
testBucketToken = "k0ow1rF9khxIMtElYfajigZYqKMAjr5-ydhcOgiUnExmiXWChMhUIAbXeOtTWA2DNR0d1jQfMpoTny25pCUrFQ=="

org = "LSBU"
url = "http://localhost:8086"

# write_api.write(bucket=bucket, org="LSBU", record=point)

client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

#connect to bucket
bucket="telemetryData"

#writing data to db
write_api = client.write_api(write_options=SYNCHRONOUS)

#querying data from db
query_api = client.query_api()
   
for value in range(5):
  point = (
    Point("measurement1")
    .tag("tagname1", "tagvalue1")
    .field("field1", value)
  )
  write_api.write(bucket=bucket, org="LSBU", record=point)
  time.sleep(1) # separate points by 1 second
"""

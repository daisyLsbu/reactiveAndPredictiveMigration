import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import json

def connectToDB():
  token = 'UnZq8-3qAHW4bk5BNjZgPJLBeeNkOXWatintbu4RAZe_96fdRbPHofP_sE6JWNEPrTnGyFUg26ofUifZQx19DA=='
  org = "LSBU"
  url = "http://localhost:8086"

  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def connectToDB_mac():
  #user/password123../master: export INFLUXDB_TOKEN=UnZq8-3qAHW4bk5BNjZgPJLBeeNkOXWatintbu4RAZe_96fdRbPHofP_sE6JWNEPrTnGyFUg26ofUifZQx19DA==/
  mastertoken = "zTXBuom_LxYD98-9gcyyDw9mHsCrtJUVVUfwsoGBxzQ3DcqwFiamo9ZtPucDfRaWEkOi-yrnqU1WFse9M67Wng=="
  #token = "eFTnKNbRWWdPmLpleqeLLhhMwkQP1FbBY1RaVPnbbDgEudRqrCNuW6Z5aVTyH2sRGMt5NgSF_Lv08PadOEKOuA=="

  #local mac
  token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  org = "LSBU"
  url = "http://localhost:8086"
  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def writeToDB(deviceData, bucket):
    client = connectToDB()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for k in deviceData:   
        print("test5")
        print("host", k['host'])
        print("cpu_count", k['cpu_count'])
        #print("nw_ip", k['nw_ip'])
        print("storage_free", k['storage_free'])
        print("vm_percent", k['vm_percent'])
        print("time", k['time'])

    for k in deviceData:
      point = (
        Point("test5")
          #.tag("host", k['host'])    # added 
          #.time(k['time'], WritePrecision.NS)
          .field("host", k['host'])
          .field("cpu_count", k['cpu_count'])
          .field("cpu_utilization", k['cpu_utilization'])
          #.field("network_drop", k['network_drop'])
          #.field("nw_ip", k['nw_ip'])
          .field("storage_free", k['storage_free'])
          .field("storage_percent", k['storage_percent'])
          .field("vm_free", k['vm_free'])
          .field("vm_percent", k['vm_percent'])
          .field("vm_used", k['vm_used'])
    )
      write_api.write(bucket=bucket, org="LSBU", record=point)

def readFromDB(bucket):
  client = connectToDB()
  res = {}
  # To create a empty set you have to use the built in method:
  victim_set = set()
  host_set = set()
  #querying data from db
  query_api = client.query_api()  
  query = """
    from(bucket: "telemetrydata")
		|> range(start: -300m)
	  |> filter(fn: (r) => r["_measurement"] == "test3")
	  |> filter(fn: (r) => r["_field"] == "cpu_count" or r["_field"] == "cpu_utilization" or r["_field"] == "network_drop")
	  |> timedMovingAverage(every: 5m, period: 10m)
    """


  tables = query_api.query(query, org="LSBU")
  results = []
  for table in tables:
      for record in table.records:
        results.append((record.get_value(), record.get_field(), record.values.get('host')))
        print(record)
        res[record['_field']] = record['_value']
        res['host'] = record['host']
        #convert to scalar value
        #compare with thresold
        #if above thresold - > #delete from host list, add into victim list 
        #host_set.remove(res['host'])
        #victim_set.add(res['host'])

  

  #print(res)
  print(results)
  

  #if victimlist is not empty - search destination host - > trigger migration
  if not victim_set:
     pass
    
              
if __name__ == '__main__':
    
    deviceData = [ 
    { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.150',
    'network_drop': 3,
    'nw_ip': '127.0.0.1',
    'storage_free': 35627315200,
    'storage_percent': 19.9,
    'time': 'Wed Jul 12 20:22:53 2023',
    'vm_free': 40894464,
    'vm_percent': 83.9,
    'vm_used': 3310534656},


  { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.150',
    'network_drop': 0,
    'nw_ip': '127.0.0.1',
    'storage_free': 35627315200,
    'storage_percent': 19.9,
    'time': 'Wed Jul 12 20:22:53 2023',
    'vm_free': 40894464,
    'vm_percent': 83.9,
    'vm_used': 3310534656}]

    bucket_mac="telemetryData"

    #writeToDB(deviceData, bucket)
    readFromDB(bucket_mac)

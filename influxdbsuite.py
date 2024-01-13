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
        print("test7")
        print("host", k['host'])
        print("cpu_count", k['cpu_count'])
        #print("nw_ip", k['nw_ip'])
        print("storage_free", k['storage_free'])
        print("vm_percent", k['vm_percent'])
        print("time", k['time'])

    for k in deviceData:
      point = (
        Point("test7")
          .tag("host", k['host'])    # added 
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

def writeToDBCombinedTest(deviceData, bucket):
    client = connectToDB()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for device in deviceData:
      point1 = (
        Point("Device")
          .tag("host", device['host'])    # added 
          .field("cpu_used", device['cpu_used'])
          .field("cpu_free", device['cpu_free'])          
          .field("cpu_percent", device['cpu_percent'])
          .field("network_drop", device['network_drop'])
          .field("storage_used", device['storage_used'])
          .field("storage_free", device['storage_free'])
          .field("storage_percent", device['storage_percent'])
          .field("vm_free", device['vm_free'])
          .field("vm_percent", device['vm_percent'])
          .field("vm_used", device['vm_used'])
        )
      if 'containers' in device:
        for container in device['containers']:
          point2 = (
            Point("Container")
            .tag("host", device['host'])    # added 
            .tag("id", container['id'])    # added 
            .field("cpu_percent", container['cpu_per'])
            .field("cpu_usage", container['cpu_usage'])
            .field("mem_percent", container['mem_per'])            
            .field("memory_usage", container['memory_usage'])
            .field("nw_percent", container['nw'])
            .field("nw_usage", container['nw_usage'])
          )
          write_api.write(bucket=bucket, org="LSBU", record=point2)

      write_api.write(bucket=bucket, org="LSBU", record=point1)


if __name__ == '__main__':

  bucket_mac="telemetrydata"

  deviceDataTest = [{
  "containers": [
    {
      "cpu_per": 0.00016619067716519125,
      "cpu_usage": 25674000,
      "id": "2a0af2fe781c",
      "mem_per": 0.1122188446225822,
      "memory_usage": 4628480,
      "nw": 0.159454345703125,
      "nw_usage": 1672
    }
  ],
  "cpu_free": 68.1,
  "cpu_percent": 31.9,
  "cpu_used": 31.9,
  "host": "192.168.1.102",
  "network_drop": 0,
  "nw_ip": "127.0.0.1",
  "storage_free": 26117939200,
  "storage_percent": 25.3,
  "storage_used": 8828182528,
  "vm_free": 23527424,
  "vm_percent": 82.2,
  "vm_used": 3770859520
}]
  writeToDBCombinedTest(deviceDataTest, bucket_mac)



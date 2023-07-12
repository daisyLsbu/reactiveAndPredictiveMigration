import influxdb_client, time
from influxdb_client import Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def connectToDB():
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
        print("nw_ip", k['nw_ip'])
        print("storage_free", k['storage_free'])
        print("vm_percent", k['vm_percent'])
        print("time", k['time'])

    for k in deviceData:
        point = (
        Point("test5")
         .tag("host", k['host'])
         .time(k['time'], WritePrecision.NS)
        .field("cpu_count", k['cpu_count'])
        .field("cpu_utilization", k['cpu_utilization'])
        .field("network_drop", k['network_drop'])
        .field("nw_ip", k['nw_ip'])
        .field("storage_free", k['storage_free'])
        .field("storage_percent", k['storage_percent'])
        .field("vm_free", k['vm_free'])
        .field("vm_percent", k['vm_percent'])
        .field("vm_used", k['vm_used'])
        )
    write_api.write(bucket=bucket, org="LSBU", record=point)
    time.sleep(1) # separate points by 1 second

if __name__ == '__main__':
    deviceData =     [ { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.150',
    'network_drop': 0,
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

    bucket="telemetryData"

    writeToDB(deviceData, bucket)
 
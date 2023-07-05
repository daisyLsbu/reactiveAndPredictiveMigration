import requests
import influxdb_client, time
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

def writeToDB(deviceData, ip):
  write_api = client.write_api(write_options=SYNCHRONOUS)
  for value in range(5):
    point = (
      Point("test3")
      .tag("host", ip)
      .field("cpu", deviceData['cpu'])
      .field("network", deviceData['network'])
      .field("storage", deviceData['storage'])
      .field("memory", deviceData['memory'])
    )
    write_api.write(bucket=bucket, org="LSBU", record=point)
    time.sleep(1) # separate points by 1 second

def connectToDB():
  token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  org = "LSBU"
  url = "http://localhost:8086"
  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def collectDataWithAPI(ip, port):
    api_url = "http://" + ip + ':' + str(port) + "/DeviceData"
    response = requests.get(api_url)
    print(response.status_code )
    if(response.status_code == 200):
        deviceData = response.json()
        writeToDB(deviceData, ip)
    else:
        print("Error getting respose")

def allHostsData():
    df = pd.read_csv('data/nodes.csv').transpose().to_dict()
    for k in df:
      print(f'ip = {df[k]["ip"]} port={df[k]["port"]} ')
      ip = df[k]["ip"]
      port = df[k]["port"]
      collectDataWithAPI(ip, port)

if __name__ == '__main__':
   client = connectToDB()
   bucket="telemetryData"

   allHostsData()
   #dummy()








"""""
def writeToDB(deviceData, ip):
  write_api = client.write_api(write_options=SYNCHRONOUS)

  for value in range(5):
    point = (
      Point("test3")
      .tag("host", ip)
      .field("cpu", deviceData['cpu'])
      .field("network", deviceData['network'])
      .field("storage", deviceData['storage'])
      .field("memory", deviceData['memory'])
    )
    write_api.write(bucket=bucket, org="LSBU", record=point)
    time.sleep(1) # separate points by 1 second
    
def connectToDB():
  token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  org = "LSBU"
  url = "http://localhost:8086"
  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def collectDataWithAPI(ip, port):
    #print(ip, po
    api_url = "http://" + ip + ':' + port + "/DeviceData"
    response = requests.get(api_url)
    #print(response.status_code)

    if(response.status_code == 200):
        deviceData = response.json()
        #print(response.json())
        #print("Local data")
        print(deviceData)
        writeToDB(deviceData, ip)
        print(deviceData['cpu'])
    else:
        print("Error getting respose")

def allHostsData():
    with open('data/nodes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            print(row)
            ip = row['ip']
            port = row['port']
            #collectDataWithAPI(ip, port)
            print(ip, port)
            writeToDB(ip, port)

def dummy():
   df = pd.read_csv('data/nodes.csv').transpose().to_dict()
   for k in df:
      print(f'ip = {df[k]["ip"]} port={df[k]["port"]} ')
"""


#connect to bucket
#bucket="telemetryData"
#client = connectToDB()

#allHostsData()
#readFromDB()
#readAggFromDB()
# writeToDB("24", "30.1.2.3")




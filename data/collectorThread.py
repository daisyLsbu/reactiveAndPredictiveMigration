import pandas as pd
import threading
#import influxdb_client, time
#from influxdb_client import Point
#from influxdb_client.client.write_api import SYNCHRONOUS

def writeToDB(deviceData, ip):
  write_api = client.write_api(write_options=SYNCHRONOUS)
  for k in deviceData:
    point = (
      Point("test4")
      .tag("host", ip)
      .field("cpu", deviceData[k]['cpu']['cpu'])
      .field("network", deviceData[k]['nw']['network'])
      .field("storage", deviceData[k]['storage']['storage'])
      .field("memory", deviceData[k]['mem']['memory'])
    )
    write_api.write(bucket=bucket, org="LSBU", record=point)
    time.sleep(1) # separate points by 1 second

def connectToDB():
  token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  org = "LSBU"
  url = "http://localhost:8086"
  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def collectDataWithAPI(ip, port, k, result):
    api_url = "http://" + ip + ':' + str(port) + "/devicedetails"
    response = requests.get(api_url)
    print(response.status_code )
    if(response.status_code == 200):
        deviceData = response.json()
        result[k] = deviceData
    else:
        print("Error getting respose")

def allHostsData():
    df = pd.read_csv('data/nodes.csv').transpose().to_dict()
    result = {}
    threads = [threading.Thread(target = collectDataWithAPI, args = (df[k]["ip"], df[k]["port"], k, result)) for k in df]
    #threads = [threading.Thread(target = getCPUData, args = (n ,result)) for n in range(0, 10)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    print(result)
    return result


if __name__ == '__main__':
    deviceData = allHostsData()
    #client = connectToDB()
    bucket="telemetryData"
    #writeToDB(deviceData, '10.0.0.0')


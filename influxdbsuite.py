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
    
def writeToDBAll(deviceData2, bucket):
    client = connectToDB_mac()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for k in deviceData2:
      point1 = (
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
      if 'ctr' in k:
        for entry in k['ctr']:
          point2 = (
            Point("test8")
            .tag("host", k['host'])    # added 
            .tag("container", entry['id'])    # added 
            .field("cpu_count", entry['ctr_cpu'])
            .field("storage_free", entry['ctr_str'])
            .field("vm_free", entry['ctr_vm'])
          )
          write_api.write(bucket=bucket, org="LSBU", record=point2)

      write_api.write(bucket=bucket, org="LSBU", record=point1)

def writeToDBCombined(deviceData3, bucket):
    client = connectToDB_mac()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    for k in deviceData3:
      point1 = (
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
      if 'containers' in k:
        for id in k['containers']:
          point2 = (
            Point("test8")
            .tag("host", k['host'])    # added 
            .tag("container", id['id'])    # added 
            .field("cpu", id["cpu_stats"]["cpu_usage"]["total_usage"])
            .field("nw", id['networks']['eth0']['rx_errors'])
            .field("vm", id["memory_stats"]["usage"])
          )
          write_api.write(bucket=bucket, org="LSBU", record=point2)

      write_api.write(bucket=bucket, org="LSBU", record=point1)

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

  deviceData = [ 
    { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.155',
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
    'host': '10.35.109.155',
    'network_drop': 0,
    'nw_ip': '127.0.0.1',
    'storage_free': 35627315200,
    'storage_percent': 19.9,
    'time': 'Wed Jul 12 20:22:53 2023',
    'vm_free': 40894464,
    'vm_percent': 83.9,
    'vm_used': 3310534656}]
        
  deviceData2 = [ 
    { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.165',
    'network_drop': 3,
    'nw_ip': '127.0.0.1',
    'storage_free': 35627315200,
    'storage_percent': 19.9,
    'time': 'Wed Jul 12 20:22:53 2023',
    'vm_free': 40894464,
    'vm_percent': 83.9,
    'vm_used': 3310534656,
    'ctr':[{'id': 49,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}]},


  { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.155',
    'network_drop': 0,
    'nw_ip': '127.0.0.1',
    'storage_free': 35627315200,
    'storage_percent': 19.9,
    'time': 'Wed Jul 12 20:22:53 2023',
    'vm_free': 40894464,
    'vm_percent': 83.9,
    'vm_used': 3310534656,
    'ctr':[{'id': 404,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}, 
    {'id': 41,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}, 
    {'id': 42,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}]}]
  
  deviceData3 = [{"containers":[{"blkio_stats":{"io_merged_recursive":'null',"io_queue_recursive":'null',"io_service_bytes_recursive":[{"major":254,"minor":0,"op":"read","value":4096},{"major":254,"minor":0,"op":"write","value":0}],"io_service_time_recursive":'null',"io_serviced_recursive":'null',"io_time_recursive":'null',"io_wait_time_recursive":'null',"sectors_recursive":'null'},"cpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195777240000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"id":"20a80e41e8c2ef2063f1f9e91667b6261650e79cf86e0159b078c994e7fc26a5","memory_stats":{"limit":4124508160,"stats":{"active_anon":0,"active_file":4096,"anon":507904,"anon_thp":0,"file":4096,"file_dirty":0,"file_mapped":0,"file_writeback":0,"inactive_anon":507904,"inactive_file":0,"kernel_stack":16384,"pgactivate":0,"pgdeactivate":0,"pgfault":5301,"pglazyfree":0,"pglazyfreed":0,"pgmajfault":0,"pgrefill":0,"pgscan":0,"pgsteal":0,"shmem":0,"slab":258712,"slab_reclaimable":167176,"slab_unreclaimable":91536,"sock":0,"thp_collapse_alloc":0,"thp_fault_alloc":0,"unevictable":0,"workingset_activate":0,"workingset_nodereclaim":0,"workingset_refault":0},"usage":856064},"name":"/agitated_goodall","networks":{"eth0":{"rx_bytes":2276,"rx_dropped":0,"rx_errors":0,"rx_packets":30,"tx_bytes":0,"tx_dropped":0,"tx_errors":0,"tx_packets":0}},"num_procs":0,"pids_stats":{"current":1,"limit":18446744073709551615},"precpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195773200000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"preread":"2023-08-05T08:37:19.267659468Z","read":"2023-08-05T08:37:20.278237885Z","storage_stats":{}}],"cpu_count":8,"cpu_utilization":15.4,"host":"10.35.84.126","network_drop":0,"nw_ip":"127.0.0.1","storage_free":17834856448,"storage_percent":33.1,"time":"Sat Aug  5 09:37:17 2023","vm_free":82952192,"vm_percent":85.0,"vm_used":3326935040}
]

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
  #writeToDBCombined(deviceData3, bucket_mac)
  #writeToDBAll(deviceData2, bucket_mac)
  #writeToDB(deviceData, bucket_mac)
  #readFromDB(bucket_mac)



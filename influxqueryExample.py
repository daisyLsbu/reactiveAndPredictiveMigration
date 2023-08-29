import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


def connectToDB():
  #token = 'UnZq8-3qAHW4bk5BNjZgPJLBeeNkOXWatintbu4RAZe_96fdRbPHofP_sE6JWNEPrTnGyFUg26ofUifZQx19DA=='
  mac_token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  org = "LSBU"
  url = "http://localhost:8086"

  client = influxdb_client.InfluxDBClient(url=url, token=mac_token, org=org)
  return client

#absolute query
query1 = """
    from(bucket:"telemetryData")
    |> range(start: -1h)
    """

#filter data on tables
query2 = """
    from(bucket:"telemetryData")
    |> range(start: -1h)
    |> filter(fn: (r) => r._measurement == "test7")
    """

#filter to get field data on tables
query3 = """
    from(bucket:"telemetryData")
    |> range(start: -1d)
    |> filter(fn: (r) => r._measurement == "test7")
    |> filter(fn: (r) => r._field == "cpu_utilization")
    |> yield()
    """

#filter to get tagdata on tables - not working
query4 = """
    from(bucket:"telemetryData")
    |> range(start: -1d)
    |> filter(fn: (r) => r._measurement == "test7" and r.tag == "host")
    |> filter(fn: (r) => r._field == "cpu_utilization")
    |> yield()
    """

#group by tag data on tables
query5 = """
    from(bucket: "telemetryData")
    |> range(start: -1d)
    |> filter(fn: (r) => r._measurement == "test7")
    |> filter(fn: (r) => r._field == "cpu_utilization")
    |> group(columns: ["host"], mode: "by")
    """

#group by tag data on tables
query6 = """
    from(bucket: "telemetryData")
	|> range(start: -1d)
    |> filter(fn: (r) => r["_measurement"] == "test101")
    |> filter(fn: (r) => r["_field"] == "host")
    """


def runquery(client, query):
  query_api = client.query_api()  
  tables = query_api.query(query, org="LSBU")

  for table in tables:
      for record in table.records:
        print(record.values)
        print(record)


def writeToDB(client, bucket):
    write_api = client.write_api(write_options=SYNCHRONOUS)

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
        

    for k in deviceData:
      point = (
        Point("test101")
          .field("host", k['host'])    # added 
          #.time(k['time'], WritePrecision.NS)
          .tag("cpu_count", k['cpu_count'])
          .tag("cpu_utilization", k['cpu_utilization'])
          #.field("network_drop", k['network_drop'])
          #.field("nw_ip", k['nw_ip'])
          .tag("storage_free", k['storage_free'])
          .tag("storage_percent", k['storage_percent'])
          .tag("vm_free", k['vm_free'])
          .tag("vm_percent", k['vm_percent'])
          .tag("vm_used", k['vm_used'])
        )
      write_api.write(bucket=bucket, org="LSBU", record=point)



client = connectToDB()
#runquery(client, query1)
#runquery(client, query2)
#runquery(client, query3)
runquery(client, query6)

#writeToDB(client, 'telemetryData')
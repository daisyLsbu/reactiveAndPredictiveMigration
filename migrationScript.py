import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

def connectToDB():
  token = 'UnZq8-3qAHW4bk5BNjZgPJLBeeNkOXWatintbu4RAZe_96fdRbPHofP_sE6JWNEPrTnGyFUg26ofUifZQx19DA=='
  org = "LSBU"
  url = "http://localhost:8086"

  client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
  return client

def readFromDB(client, bucket):
  
  res = {}

  # To create a empty set you have to use the built in method:
  victim_set = {}
  host_set={}

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
      records = {}
      for record in table.records:
        if record.value('host') in records:
           records[record.value('host')].appended({record.get_field() : record.get_value()})
        else:
           records[record.value('host')]:[{record.get_field() : record.get_value()}]   
        pp.pprint(record)
        res[record['_field']] = record['_value']
        res['host'] = record['host']
        #convert to scalar value
        #compare with thresold
        #if above thresold - > #delete from host list, add into victim list 
        #host_set.remove(res['host'])
        #victim_set.add(res['host'])

  

  #print(res)
  #print(results)
  

  #if victimlist is not empty - search destination host - > trigger migration
  if not victim_set:
     pass   
              
if __name__ == '__main__':
    
    bucket="telemetrydata"
    client = connectToDB()
    while(1):
        readFromDB(client, bucket)


"""
import nodeSelection
import hostSelection
import connectRemote

def migrate():
    victim = nodeSelection.getvictim()
    host = hostSelection.gethost()

    connectRemote.ssh(victim.ip, victim.user, victim.pw, 'migrateVictim.py', victim.id)

    #if success
    connectRemote.ssh(host.ip, host.user, host.pw, 'restoreimage.py', victim.id)
"""





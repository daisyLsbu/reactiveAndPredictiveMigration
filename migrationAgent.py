import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from pprint import PrettyPrinter

'''
This module reads the moving average value of all the host from influx db
compares with the threshold and if above threshold, adds the host to victim_set 
for each host in victim_set: gets flagged container from json and rtt values wrt all other host
for all host in host_set: gets available resources
for each flagged containers, get required resources, compares with available resources of host_set
if matched, available resource of host_set is reduced and migration is triggered.

data: victim_set, dest_set, dest_rtt, dest_resource, cntr_resource

'''

pp = PrettyPrinter(indent=2)
victim_set = set()
dest_set = set()
dest_rtt = {}
dest_resource = {} 
cntr_resource = {}

dbdata= {}
thresold = 20

def connectToDB():
  #token = 'UnZq8-3qAHW4bk5BNjZgPJLBeeNkOXWatintbu4RAZe_96fdRbPHofP_sE6JWNEPrTnGyFUg26ofUifZQx19DA=='
  mac_token = "tKQMaN6mMBXH-gDotw6qvpEOvcZNIMILQWTH1LTKFDddf3e4owp48cG88bFae1L_H3H5Tp8GV0jrDdzBjQiRhQ=="
  org = "LSBU"
  url = "http://localhost:8086"
  client = influxdb_client.InfluxDBClient(url=url, token=mac_token, org=org)
  return client

def readFromDB(client, bucket):
  
  # To create a empty set, the built in method is used:
  victim_set = set()
  dest_set = set()
  dbdata= {}
  thresold = 20

  #querying data from db
  query_api = client.query_api()  

  query = """
  from(bucket: "telemetryData")
	|> range(start: -1d)
  |> filter(fn: (r) => r["_measurement"] == "test7")
  |> filter(fn: (r) => r["_field"] == "cpu_utilization" or r["_field"] == "storage_free" or r["_field"] == "vm_free")
  |> filter(fn: (r) => r["host"] == "10.35.109.155")
  """

  tables = query_api.query(query, org="LSBU")

  for table in tables:
      for record in table.records:

        dest_set.add(record['host'])
       
        if record['host'] in dbdata:
          dbdata[record['host']].update({record['_field'] : record['_value']})        
        else:
           dbdata[record['host']] = {record['_field'] : record['_value']} 
           
  print(dbdata) 
  print(dest_set)   

  #convert to scalar value
  for host in dest_set:
    cumulativeValue = dbdata[host]['cpu_utilization'] + dbdata[host]['storage_free'] + dbdata[host]['storage_free']
    print(cumulativeValue)

    #compare with thresold
    if cumulativeValue > thresold:
      #if above thresold - > #delete from dest_set, add into victim list 
      victim_set.add(host)  
      print(victim_set)
      #remove victim from host set
      #host_set.remove(victim_set)
      #print(host_set)   
  
  #if victimlist is not empty - search victim container and destination host - > trigger migration
  if not victim_set:
     pass
  #else:
     #updateVictimContainers()
     #selecthostandtriggerMigration()
              
if __name__ == '__main__':
    
    bucket="telemetrydata"
    client = connectToDB()
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





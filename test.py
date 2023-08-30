import pandas as pd
import requests
import connectRemote
'''
updates dest_resource and cntr_resource with flagged containers
updates dest_rtt data
calls API to get telemetry data, containerdata as well as RTT data
'''

victim_set = set()
dest_set = set()
deviceData = []
rttData = []
dest_resource = {} 
cntr_resource = {}
dest_rtt = {}


#update the dest_resource with the available resource details
def updateDestResource(host, cpu_utilization):
    dest_resource[host] = {'cpu':cpu_utilization} 

#update the cntr_resource with the available resource details
def updateVictimCntrResource(host, container, cpu, nw, vm):
    cntr_resource[container] = {'cpu':cpu, 'nw':nw, 'vm':vm, 'host':host } 

#update the rtt data for victim nodes to available destination nodes
def updateRttData(rttData, victim):
    for dest in rttData:
        if victim in dest_rtt:
            dest_rtt[victim].update({dest['host'] : dest['avg_latency']})
        else:
            dest_rtt[victim] = {dest['host'] : dest['avg_latency']}

#checks if a container can be flagged as victim and updates it's resource requirement
def checkCntrResource(cntr, host):
     for id in cntr:
            cpu = id["cpu_stats"]["cpu_usage"]["total_usage"]
            nw = id['networks']['eth0']['rx_errors']
            vm = id["memory_stats"]["usage"]
            container = id['id']
            if cpu+nw+vm > 2000:
                updateVictimCntrResource(host, container, cpu, nw, vm)

#takes the combined API return value to update both victim and destination resources
def updateResourceDetails(deviceData3):
    for k in deviceData3:
        if k['host'] in dest_set:
            updateDestResource(k['host'], k['cpu_utilization'])
            
        elif k['host'] in victim_set:
         if 'containers' in k:
          checkCntrResource(k['containers'], k['host'])

def getRTTforVictim():
    # for all hosts in victim_set 
    for victim in victim_set:
        #call api and get values
        rttData = [{'host': '8.8.8.8', 'avg_latency': 6.32, 'min_latency': 5.98, 'max_latency': 6.7, 'packet_loss': 0.0}, 
                   {'host': '8.8.8.5', 'avg_latency': 6.20, 'min_latency': 5.98, 'max_latency': 6.7, 'packet_loss': 0.0}, 
                   {'host': '8.8.8.5', 'avg_latency': 6.12, 'min_latency': 5.98, 'max_latency': 6.7, 'packet_loss': 0.0}, 
                   {'host': '10.35.84.127', 'avg_latency': 6.20, 'min_latency': 5.98, 'max_latency': 6.7, 'packet_loss': 0.0}, 
                   {'host': '10.35.84.128', 'avg_latency': 6.12, 'min_latency': 5.98, 'max_latency': 6.7, 'packet_loss': 0.0}
                   ]
        updateRttData(rttData, victim)
    
def getResourceDataWithAPI():
    df = pd.read_csv('data/nodes.csv').transpose().to_dict()
    for k in df:
      print(f'ip = {df[k]["ip"]} port={df[k]["port"]} ')
      ip = df[k]["ip"]
      port = df[k]["port"]
      api_url = "http://" + ip + ':' + str(port) + "/DeviceData"
      response = requests.get(api_url)
      print(response.status_code )
      if(response.status_code == 200):
        jsonData = response.json()
        deviceData.append(jsonData)
      else:
        print("Error getting respose")

def selectBestRTTValue(list, srcIP):
    print(srcIP)
    print(dest_rtt)
    if srcIP in dest_rtt:
        rtt_values = dest_rtt[srcIP]
        # Creating a new dictionary with only the desired keys
        filtered_rtt = {key: value for key, value in rtt_values.items() if key in list}
        lowest_rtt = min(filtered_rtt.values())
        dest_IP = [key for key, value in filtered_rtt.items() if value == lowest_rtt][0]
    return dest_IP
'''
def selectDestToMigrate(demand, srcIP):
    IPlist = []
    for key in dest_resource:
        avail = dest_resource[key]
        if(demand['cpu'] > avail['cpu']):
            IPlist.append(key)
    print(IPlist)
    destIP = selectBestRTTValue(IPlist, srcIP)
    return destIP
'''

def copyToDestination(destIP):
    pass


def migrateVictimCntr():
    cntrId = ''
    srcIP = ''
    destIP = ''
    for key in cntr_resource:
        cntrId = key
        srcIP = cntr_resource[key]['host']
        demand = cntr_resource[key]
        IPlist = []
        for key in dest_resource:
            avail = dest_resource[key]
            if(demand['cpu'] > avail['cpu']):
                IPlist.append(key)
        destIP = selectBestRTTValue(IPlist, srcIP)
        createSourceImage(srcIP, cntrId)
        copyToDestination(destIP)
        restoreInDestination(destIP)

def createSourceImage(srcIP, cntrId):
    connectRemote.sshmigrate(srcIP, cntrId)

def restoreInDestination(destIP):
    connectRemote.sshrestore(destIP)
            
if __name__ == '__main__':
    cntrId = 'a26f6bb7336b'
    srcIP = "192.168.122.210"
    destIP = "192.168.122.210"
    # createSourceImage(srcIP, cntrId)
    restoreInDestination(destIP)









if __name__ == 'none':
    # data for testing
    deviceData3 = [{"containers":[{"blkio_stats":{"io_merged_recursive":'null',"io_queue_recursive":'null',"io_service_bytes_recursive":[{"major":254,"minor":0,"op":"read","value":4096},{"major":254,"minor":0,"op":"write","value":0}],"io_service_time_recursive":'null',"io_serviced_recursive":'null',"io_time_recursive":'null',"io_wait_time_recursive":'null',"sectors_recursive":'null'},"cpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195777240000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"id":"20a80e41e8c2ef2063f1f9e91667b6261650e79cf86e0159b078c994e7fc26a5","memory_stats":{"limit":4124508160,"stats":{"active_anon":0,"active_file":4096,"anon":507904,"anon_thp":0,"file":4096,"file_dirty":0,"file_mapped":0,"file_writeback":0,"inactive_anon":507904,"inactive_file":0,"kernel_stack":16384,"pgactivate":0,"pgdeactivate":0,"pgfault":5301,"pglazyfree":0,"pglazyfreed":0,"pgmajfault":0,"pgrefill":0,"pgscan":0,"pgsteal":0,"shmem":0,"slab":258712,"slab_reclaimable":167176,"slab_unreclaimable":91536,"sock":0,"thp_collapse_alloc":0,"thp_fault_alloc":0,"unevictable":0,"workingset_activate":0,"workingset_nodereclaim":0,"workingset_refault":0},"usage":856064},"name":"/agitated_goodall","networks":{"eth0":{"rx_bytes":2276,"rx_dropped":0,"rx_errors":0,"rx_packets":30,"tx_bytes":0,"tx_dropped":0,"tx_errors":0,"tx_packets":0}},"num_procs":0,"pids_stats":{"current":1,"limit":18446744073709551615},"precpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195773200000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"preread":"2023-08-05T08:37:19.267659468Z","read":"2023-08-05T08:37:20.278237885Z","storage_stats":{}}],"cpu_count":8,"cpu_utilization":15.4,"host":"10.35.84.126","network_drop":0,"nw_ip":"127.0.0.1","storage_free":17834856448,"storage_percent":33.1,"time":"Sat Aug  5 09:37:17 2023","vm_free":82952192,"vm_percent":85.0,"vm_used":3326935040}, {"containers":[{"blkio_stats":{"io_merged_recursive":'null',"io_queue_recursive":'null',"io_service_bytes_recursive":[{"major":254,"minor":0,"op":"read","value":4096},{"major":254,"minor":0,"op":"write","value":0}],"io_service_time_recursive":'null',"io_serviced_recursive":'null',"io_time_recursive":'null',"io_wait_time_recursive":'null',"sectors_recursive":'null'},"cpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195777240000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"id":"20a80e41e8c2ef2063f1f9e91667b6261650e79cf86e0159b078c994e7fc26b5","memory_stats":{"limit":4124508160,"stats":{"active_anon":0,"active_file":4096,"anon":507904,"anon_thp":0,"file":4096,"file_dirty":0,"file_mapped":0,"file_writeback":0,"inactive_anon":507904,"inactive_file":0,"kernel_stack":16384,"pgactivate":0,"pgdeactivate":0,"pgfault":5301,"pglazyfree":0,"pglazyfreed":0,"pgmajfault":0,"pgrefill":0,"pgscan":0,"pgsteal":0,"shmem":0,"slab":258712,"slab_reclaimable":167176,"slab_unreclaimable":91536,"sock":0,"thp_collapse_alloc":0,"thp_fault_alloc":0,"unevictable":0,"workingset_activate":0,"workingset_nodereclaim":0,"workingset_refault":0},"usage":856064},"name":"/agitated_goodall","networks":{"eth0":{"rx_bytes":2276,"rx_dropped":0,"rx_errors":0,"rx_packets":30,"tx_bytes":0,"tx_dropped":0,"tx_errors":0,"tx_packets":0}},"num_procs":0,"pids_stats":{"current":1,"limit":18446744073709551615},"precpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195773200000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"preread":"2023-08-05T08:37:19.267659468Z","read":"2023-08-05T08:37:20.278237885Z","storage_stats":{}}],"cpu_count":8,"cpu_utilization":15.4,"host":"10.35.84.127","network_drop":0,"nw_ip":"127.0.0.1","storage_free":17834856448,"storage_percent":33.1,"time":"Sat Aug  5 09:37:17 2023","vm_free":82952192,"vm_percent":85.0,"vm_used":3326935040}, {"containers":[{"blkio_stats":{"io_merged_recursive":'null',"io_queue_recursive":'null',"io_service_bytes_recursive":[{"major":254,"minor":0,"op":"read","value":4096},{"major":254,"minor":0,"op":"write","value":0}],"io_service_time_recursive":'null',"io_serviced_recursive":'null',"io_time_recursive":'null',"io_wait_time_recursive":'null',"sectors_recursive":'null'},"cpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195777240000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"id":"20a80e41e8c2ef2063f1f9e91667b6261650e79cf86e0159b078c994e7fc26b5","memory_stats":{"limit":4124508160,"stats":{"active_anon":0,"active_file":4096,"anon":507904,"anon_thp":0,"file":4096,"file_dirty":0,"file_mapped":0,"file_writeback":0,"inactive_anon":507904,"inactive_file":0,"kernel_stack":16384,"pgactivate":0,"pgdeactivate":0,"pgfault":5301,"pglazyfree":0,"pglazyfreed":0,"pgmajfault":0,"pgrefill":0,"pgscan":0,"pgsteal":0,"shmem":0,"slab":258712,"slab_reclaimable":167176,"slab_unreclaimable":91536,"sock":0,"thp_collapse_alloc":0,"thp_fault_alloc":0,"unevictable":0,"workingset_activate":0,"workingset_nodereclaim":0,"workingset_refault":0},"usage":856064},"name":"/agitated_goodall","networks":{"eth0":{"rx_bytes":2276,"rx_dropped":0,"rx_errors":0,"rx_packets":30,"tx_bytes":0,"tx_dropped":0,"tx_errors":0,"tx_packets":0}},"num_procs":0,"pids_stats":{"current":1,"limit":18446744073709551615},"precpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195773200000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"preread":"2023-08-05T08:37:19.267659468Z","read":"2023-08-05T08:37:20.278237885Z","storage_stats":{}}],"cpu_count":8,"cpu_utilization":15.4,"host":"10.35.84.128","network_drop":0,"nw_ip":"127.0.0.1","storage_free":17834856448,"storage_percent":33.1,"time":"Sat Aug  5 09:37:17 2023","vm_free":82952192,"vm_percent":85.0,"vm_used":3326935040}
    ]

    #setting values to test
    dest_set.add('10.35.84.127') 
    dest_set.add('10.35.84.128') 

    victim_set.add('10.35.84.126') 

    #call combined API to get real data instead of test data
    #ßgetResourceDataWithAPI()

    #updates details
    updateResourceDetails(deviceData3)
    getRTTforVictim()

    #print updated resource after test
    print(dest_resource)
    print(cntr_resource)
    print(dest_rtt)

    migrateVictimCntr()

  

  
'''
testing json file : create, read and write
append and update, delete
'''
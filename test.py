import dict

deviceData2 = { 'cpu_count': 8,
    'cpu_utilization': 5.3,
    'host': '10.35.109.155',
    'network_drop': 3,
    'nw_ip': '127.0.0.1',
    'storage_free': 35627315200,
    'storage_percent': 19.9,
    'time': 'Wed Jul 12 20:22:53 2023',
    'vm_free': 40894464,
    'vm_percent': 83.9,
    'vm_used': 3310534656,
    'ctr': {'id': 4089,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}}

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
    'vm_used': 3310534656,
    'ctr': {'id': 4089,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}},


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
    'ctr':{'id': 4089,
    'ctr_cpu': 83.9,
    'ctr_str': 83.9,
    'ctr_vm': 3310534656}}]

people = {1: {'name': 'John', 'age': '27', 'sex': 'Male'},
          2: {'name': 'Marie', 'age': '22', 'sex': 'Female'}}

print(people[1]['name'])
print(people[1]['age'])
print(people[1]['sex'])

print(deviceData2['cpu_utilization'])
print(deviceData2['ctr']['id'])

for entry in deviceData:
    print(entry['cpu_utilization'])
    print(entry['ctr']['id'])

dict1 = {'X':[1, 2, 3], 'Y':[4, 5, 6]}
dict1['X'].append(12)
print(dict1)

docker1 = {'ctr':[1, 2, {"major":254}], 'Y':[4, 5, 6]}
print(docker1)
print(docker1['ctr'])

docker2 = {'ctr':[{"major":254,"minor":0,"op":"read","value":4096}], 'Y':[4, 5, 6]}
print(docker2['ctr'])

for k in docker2['ctr']:
    print(k['major'])

docker3 = [{'ctr':[{"major":254,"minor":0,"op":"read","value":4096}, {"major":223,"minor":0,"op":"read","value":4096}], 'Y':[4, 5, 6]}]

for doc in docker3:
    for k in doc['ctr']:
        print(k['major'])

#check if key exists:
docker4 = [{'ctr':[{"major":254,"minor":0,"op":"read","value":4096}, {"major":223,"minor":0,"op":"read","value":4096}], 'Y':[4, 5, 6]}]
print('docker4')

for doc in docker4:
  if 'ctr' in doc:
    for k in doc['ctr']:
        print(k['major'])

docker5 = {"containers":[{"blkio_stats":{"io_merged_recursive":'null',"io_queue_recursive":'null',"io_service_bytes_recursive":[{"major":254,"minor":0,"op":"read","value":4096},{"major":254,"minor":0,"op":"write","value":0}],"io_service_time_recursive":'null',"io_serviced_recursive":'null',"io_time_recursive":'null',"io_wait_time_recursive":'null',"sectors_recursive":'null'},"cpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195777240000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"id":"20a80e41e8c2ef2063f1f9e91667b6261650e79cf86e0159b078c994e7fc26a5","memory_stats":{"limit":4124508160,"stats":{"active_anon":0,"active_file":4096,"anon":507904,"anon_thp":0,"file":4096,"file_dirty":0,"file_mapped":0,"file_writeback":0,"inactive_anon":507904,"inactive_file":0,"kernel_stack":16384,"pgactivate":0,"pgdeactivate":0,"pgfault":5301,"pglazyfree":0,"pglazyfreed":0,"pgmajfault":0,"pgrefill":0,"pgscan":0,"pgsteal":0,"shmem":0,"slab":258712,"slab_reclaimable":167176,"slab_unreclaimable":91536,"sock":0,"thp_collapse_alloc":0,"thp_fault_alloc":0,"unevictable":0,"workingset_activate":0,"workingset_nodereclaim":0,"workingset_refault":0},"usage":856064},"name":"/agitated_goodall","networks":{"eth0":{"rx_bytes":2276,"rx_dropped":0,"rx_errors":0,"rx_packets":30,"tx_bytes":0,"tx_dropped":0,"tx_errors":0,"tx_packets":0}},"num_procs":0,"pids_stats":{"current":1,"limit":18446744073709551615},"precpu_stats":{"cpu_usage":{"total_usage":167978000,"usage_in_kernelmode":114098000,"usage_in_usermode":53879000},"online_cpus":4,"system_cpu_usage":195773200000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"preread":"2023-08-05T08:37:19.267659468Z","read":"2023-08-05T08:37:20.278237885Z","storage_stats":{}}],"cpu_count":8,"cpu_utilization":15.4,"host":"10.35.84.126","network_drop":0,"nw_ip":"127.0.0.1","storage_free":17834856448,"storage_percent":33.1,"time":"Sat Aug  5 09:37:17 2023","vm_free":82952192,"vm_percent":85.0,"vm_used":3326935040}

if 'containers' in docker5:
    for id in docker5['containers']:
        print(id["cpu_stats"]["cpu_usage"]["total_usage"])
        print(id['id'])
        print(id["memory_stats"]["usage"])
        print(id["storage_stats"])
        print(id['networks']['eth0']['rx_errors'])
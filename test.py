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
import psutil

def getCPUData():
    cpu = psutil.cpu_percent(interval=2)
    dataIns = cpuData(cpu)
    return dataIns

def getMemoryData():
    memory = psutil.virtual_memory().percent

    dataIns = memoryData(memory)
    return dataIns

def getStorageData():
    storage = psutil.disk_usage('/').percent

    dataIns = storageData( storage)
    return dataIns

def getNetworkData():
    network = psutil.net_io_counters().dropout

    dataIns = networkData(network)
    return dataIns


class cpuData(dict):

    def __init__(self, cpu):
        dict.__init__(self, cpu=cpu)
        
    def get(self):
        return self.cpu
    
class memoryData(dict):

    def __init__(self, memory):
        dict.__init__(self, memory=memory)
        
    def get(self):
        return self.memory
    
class storageData(dict):

    def __init__(self, storage):
        dict.__init__(self, storage=storage)
        
    def get(self):
        return self.storage
    
class networkData(dict):

    def __init__(self, network):
        dict.__init__(self, network=network)
        
    def get(self):
        return self.network


def getTelemtryData():
    cpu = psutil.cpu_percent(interval=2)
    memory = psutil.virtual_memory().percent
    storage = psutil.disk_usage('/').percent
    network = psutil.net_io_counters().dropout

    dataIns = telemetryData(cpu, memory, storage, network)
    return dataIns

"""""
#getTelemtryData()
print(psutil.cpu_percent(interval=2))
print(psutil.cpu_count())
#print(psutil.cpu_freq().max)
#print(psutil.cpu_freq().current)



print(psutil.virtual_memory().percent)
print(psutil.virtual_memory().used)
print(psutil.virtual_memory().free)


print(psutil.disk_usage('/').percent)
print(psutil.disk_usage('/').free)


print(psutil.net_io_counters().dropout)
#print(psutil.net_connections(kind='inet4').__getattribute__)
#print(psutil.net_if_addrs())
count = 0
for name, stats in psutil.net_if_addrs().items():
    print(count)
    print(name, stats)
    count = count +1

count = 0
for name, stats in psutil.net_connections(kind='inet4').items():
    print(count)
    print(name, stats)
    count = count +1

"""
nic = psutil.net_if_addrs()
addrs = nic['lo0']

for addr in addrs:
    if addr.family._name_.__eq__('AF_INET') != 0:
        print(" family   : %s" % addr.family._name_)
        print(" address   : %s" % addr.address)
        print(getattr(addr, "address"))



import socket   
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname) 


import socket
 
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
 
local_ip = get_local_ip()
print(local_ip)

import datetime;
 
# ct stores current time
ct = datetime.datetime.now()
print("current time:-", ct)



#for nic, addrs in psutil.net_if_addrs().items():
    #if nic == 'lo'
        #print("%s:" % (nic))


#getattr(psutil.net_if_addrs(), "snicaddr")



"""""
    appData1 = telemetryData(1,2,3,4)
    appData1.setCPU(10)
    appData1.setMemory(15)
    appData1.setStorage(20)
    appData1.setNetwork(25)
"""

"""""
#import time
#import platform
psutil.cpu_times_percent
psutil.virtual_memory

print(platform.processor())
print(psutil.cpu_percent(interval=2))
print(psutil.virtual_memory)
print(psutil.net_connections)

#create class instance and test
appData1 = telemetryData(2,3,4,5)
appData1.setCPU(10)
appData1.setMemory(15)
appData1.setStorage(20)
appData1.setNetwork(25)

#get object details
print(appData1)
print(appData1.getCPU())
print(appData1.getMemory())
print(appData1.getStorage())
print(appData1.getNetwork())

appData2 = getTelemtryData()
print(appData2.getCPU())
print(appData2.getMemory())
print(appData2.getStorage())
print(appData2.getNetwork())
"""





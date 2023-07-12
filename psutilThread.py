import threading 
import psutil
import socket
import datetime;

resourceData = {}

class cpuData:
        
    def getCPUData(self):
        cpu_utilization  = psutil.cpu_percent(interval=2)
        cpu_count = psutil.cpu_count()
        #cpu_freq_max = psutil.cpu_freq().max
        #cpu_freq_cur = psutil.cpu_freq().current
        global resourceData
        resourceData['cpu_utilization'] = cpu_utilization
        resourceData['cpu_count'] = cpu_count
        #resourceData['cpu_freq_max'] = cpu_freq_max
        #resourceData['cpu_freq_cur'] = cpu_freq_cur

class memoryData:

    def getMemoryData(self):
        vm_percent = psutil.virtual_memory().percent
        vm_used = psutil.virtual_memory().used
        vm_free = psutil.virtual_memory().free
        global resourceData
        resourceData['vm_percent'] = vm_percent
        resourceData['vm_used'] = vm_used
        resourceData['vm_free'] = vm_free

    
class storageData:

    def getStorageData(self):
        storage_percent = psutil.disk_usage('/').percent
        storage_free = psutil.disk_usage('/').free
        global resourceData
        resourceData['storage_percent'] = storage_percent
        resourceData['storage_free'] = storage_free

    
class networkData:

    def getNetworkData(self):
        network_drop = psutil.net_io_counters().dropout
        nic = psutil.net_if_addrs()
        addrs = nic['lo0']
        for addr in addrs:
            if addr.family._name_.__eq__('AF_INET') != 0:
                nw_ip = getattr(addr, "address")
        global resourceData
        resourceData['network_drop'] = network_drop
        resourceData['nw_ip'] = nw_ip

        '''''
count = 0
for name, stats in psutil.net_connections(kind='inet4').items():
    print(count)
    print(name, stats)
    count = count +1
    '''
        
 
def get_local_ip_time():
 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    resourceData['host'] = IP
    resourceData['time'] = datetime.datetime.now().ctime()
 
def startThreads():
    cpu = cpuData()
    mem = memoryData()
    stg = storageData()
    nw = networkData()

    t1 = threading.Thread(target = cpu.getCPUData, args = ())
    t2 = threading.Thread(target = mem.getMemoryData, args = ())
    t3 = threading.Thread(target = stg.getStorageData, args = ())
    t4 = threading.Thread(target = nw.getNetworkData, args = ())
    t5 = threading.Thread(target = get_local_ip_time, args = ())

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()

    return resourceData

if __name__ == '__main__':
    
    print(startThreads())

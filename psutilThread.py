import threading 
import psutil

resourceData = {}

class cpuData:
        
    def getCPUData(self):
        cpu = psutil.cpu_percent(interval=2)
        global resourceData
        resourceData['cpu'] = cpu

class memoryData:

    def getMemoryData(self):
        memory = psutil.virtual_memory().percent
        global resourceData
        resourceData['memory'] = memory
    
class storageData:

    def getStorageData(self):
        storage = psutil.disk_usage('/').percent
        global resourceData
        resourceData['storage'] = storage
    
class networkData:

    def getNetworkData(self):
        network = psutil.net_io_counters().dropout
        global resourceData
        resourceData['network'] = network

def startThreads():
    cpu = cpuData()
    mem = memoryData()
    stg = storageData()
    nw = networkData()

    t1 = threading.Thread(target = cpu.getCPUData, args = ())
    t2 = threading.Thread(target = mem.getMemoryData, args = ())
    t3 = threading.Thread(target = stg.getStorageData, args = ())
    t4 = threading.Thread(target = nw.getNetworkData, args = ())

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

if __name__ == '__main__':
    startThreads()
    print(resourceData)

import threading 
import psutil

def getCPUData(num, result):
    cpu = psutil.cpu_percent(interval=2)
    dataIns = cpuData(cpu)
    result[num] = dataIns

def getMemoryData(num, result):
    memory = psutil.virtual_memory().percent

    dataIns = memoryData(memory)
    result[num] =  dataIns

def getStorageData(num, result):
    storage = psutil.disk_usage('/').percent

    dataIns = storageData( storage)
    result[num] =  dataIns

def getNetworkData(num, result):
    network = psutil.net_io_counters().dropout

    dataIns = networkData(network)
    result[num] =  dataIns


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

"""""
def getCPUData(num, result):
    cpu = psutil.cpu_percent(interval=2)
    result[num] = cpu

def getMemoryData(num, result):
    memory = psutil.virtual_memory().percent
    result[num] = memory
def getStorageData(num, result):
    storage = psutil.disk_usage('/').percent
    result[num] = storage

def getNetworkData(num, result):
    network = psutil.net_io_counters().dropout
    result[num] = network
"""
def startThreads():
    result = {}

    t1 = threading.Thread(target = getCPUData, args = ('cpu',result))
    t2 = threading.Thread(target = getMemoryData, args = ('mem',result))
    t3 = threading.Thread(target = getStorageData, args = ('storage',result))
    t4 = threading.Thread(target = getNetworkData, args = ('nw',result))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    return result


if __name__ == '__main__':
    result = startThreads()
    print(result)
    print(result['mem']['memory'])

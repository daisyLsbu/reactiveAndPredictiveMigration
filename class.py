import psutil

first_list = []
second_list = {}
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

class MyClass:
    def change_values(self):
        first_list.append('cat')
        #second_list[:] = ['cat']
        global second_list
        second_list['cat'] = 10


test = MyClass()
test.change_values()
print(first_list)
print(second_list)

test1 = cpuData()
test1.getCPUData()
test2 = memoryData()
test2.getMemoryData()
test3 = storageData()
test3.getStorageData()
test4 = networkData()
test4.getNetworkData()
print(resourceData)

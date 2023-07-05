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

class telemetryData(dict):

    def __init__(self, cpu, memory, storage, network):
        dict.__init__(self, cpu=cpu, memory=memory, storage=storage, network=network)
    
    def setCPU(self, value):
        self.cpu = value
    
    def setMemory(self, value):
        self.memory = value
    
    def setStorage(self, value):
        self.storage = value
    
    def setNetwork(self, value):
        self.network = value

    def getCPU(self):
        return self.cpu
    
    def getMemory(self):
        return self.memory
    
    def getStorage(self):
        return self.storage
    
    def getNetwork(self):
        return self.network

"""  
#create class instance and test
appData1 = telemetryData(10,13,15,11)
#set values
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
#print(jsonify(appData1))
import json
print(json.dumps(appData1))
"""

#create class instance and test
Data1 = cpuData(10)
Data2 = memoryData(13)
Data3 = storageData(15)
Data4 = networkData(11)


#get object details
print(Data1)
print(Data2)
print(Data3)
print(Data4)

merged = dict()

merged.update(Data1)
merged.update(Data2)
merged.update(Data3)
merged.update(Data4)


print(merged)

import psutil
from telemetryData import telemetryData

def getTelemtryData():
    cpu = psutil.cpu_percent(interval=2)
    memory = psutil.virtual_memory().percent
    storage = psutil.disk_usage('/').percent
    network = psutil.net_io_counters().dropout

    dataIns = telemetryData(cpu, memory, storage, network)
    return dataIns

#ßgetTelemtryData()


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





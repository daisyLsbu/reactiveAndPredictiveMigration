import threading 
import psutil
import socket
import datetime;

resourceData = {}

class cpuData:
        
    def getCPUData(self):
        """
        This method returns the CPU usage data.
        It uses 'psutil' module to fetch this information.
        :return: A dictionary containing the following details -
        1) "cpu_percent" : The percentage of CPU used by the process since it started
        2) "times"       : A tuple representing the number of seconds spent in user mode,
        kernel mode, and idle mode respectively.
        """
        cpu_percent  = psutil.cpu_percent(interval=2)
        used_cpu_capacity = cpu_percent
        free_cpu_capacity = 100 - used_cpu_capacity
        #cpu_count = psutil.cpu_count()
        #cpu_freq_max = psutil.cpu_freq().max
        #cpu_freq_cur = psutil.cpu_freq().current
        global resourceData
        resourceData['cpu_percent'] = cpu_percent
        resourceData['cpu_used'] = used_cpu_capacity
        resourceData['cpu_free'] = free_cpu_capacity
        #resourceData['cpu_freq_max'] = cpu_freq_max
        #resourceData['cpu_freq_cur'] = cpu_freq_cur

class memoryData:

    def getMemoryData(self):
        """
        This method returns the Memory Usage Data.
        It uses 'psutil' module to fetch this information.
        :return: A dictionary containing the following details -
        1) "total" : Total physical memory available on the system.
        2) "available" : Available physical memory on the system.
        """
        vm_percent = psutil.virtual_memory().percent
        vm_used = psutil.virtual_memory().used
        vm_free = psutil.virtual_memory().free
        global resourceData
        resourceData['vm_percent'] = vm_percent
        resourceData['vm_used'] = vm_used
        resourceData['vm_free'] = vm_free

    
class storageData:

    def getStorageData(self):
        """
        This method returns the Storage I/O statistics.
        It uses 'psutil' module to fetch this information.
        The returned data is a list of dictionaries with each dictionary representing one disk drive.
        Each dictionary contains the following details about that particular disk drive -
        1)"device" : Name or path of the device e.g., "/dev/s
        2)"mountpoint" : Directory where the filesystem of the device is mounted, e.g
        "/".
        """
        storage_percent = psutil.disk_usage('/').percent
        storage_free = psutil.disk_usage('/').free
        storage_used = psutil.disk_usage('/').used
        global resourceData
        resourceData['storage_percent'] = storage_percent
        resourceData['storage_free'] = storage_free
        resourceData['storage_used'] = storage_used

    
class networkData:

    def getNetworkData(self):
        """
        This method returns Network IO Statistics.
        It uses 'socket' and 'psutil' modules to fetch this information.
        The returned data is a dictionary containing the following details -
        1)"name" : Name of the interface (e.g., eth0).
        2)"ip" : IP address assigned for that interface.
        3)"netmask" : Netmask of the IP address.
        4)"mac" : MAC address of the interface.
        5)"speed" : Speed of the interface in Mbps.
        6)"type" : Type of the interface (Ethernet, Wireless etc.).
        """
        network_drop = psutil.net_io_counters().dropout
        global resourceData
        resourceData['network_drop'] = network_drop
        resourceData['nw_ip'] = "127.0.0.1"
        
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
 
def startThreads():
    """
    Starts the threads for getting CPU and memory data every second.
    """
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

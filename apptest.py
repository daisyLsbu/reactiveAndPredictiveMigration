import psutilThread 
import dockerStat
import sys

def get_deviceDetails():
   result = psutilThread.startThreads()
   return result

def get_containersDetails():
   result = dockerStat.dockerstatinfo()
   return result

def get_combineddata():
    result = psutilThread.startThreads()
    result['containers'] = dockerStat.dockerstatinfo()
    return result

if __name__ == '__main__':
   #print(get_deviceDetails())
   #print(get_containersDetails())
   print(get_combineddata())
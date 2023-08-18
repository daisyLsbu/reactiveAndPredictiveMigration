import subprocess
import json
from json import JSONEncoder

def subprocesswithinput():
    host = input("Enter Host: ")
   # packet = int(input("\nEnter Packet: "))
    print("\n")
    ping = subprocess.getoutput(f"ping {host}")
    print(ping)

class testjsonencoder():
    _len = 4

    def __init__(self, atttr):
        self.attr = atttr

# subclass JSONEncoder
class testEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__

if __name__ == '__main__':
    objtest = testjsonencoder(350)
    print(objtest.attr)
    print(objtest._len)
    print(testjsonencoder._len)
    objtest._len = 23
    objtest.attr = 666
    print(objtest.attr)
    print(objtest._len)
    print(testjsonencoder._len)

    jsonstring = json.dumps(objtest, cls= testEncoder)


    print(jsonstring)
    print('i m main')
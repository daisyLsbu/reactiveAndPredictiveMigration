import csv
import requests

def collectDataWithAPI(ip, port):
    #print(ip, port)
    api_url = "http://" + ip + ':' + port + "/DeviceData"
    response = requests.get(api_url)
    #print(response.status_code)

    if(response.status_code == 200):
        deviceData = response.json()
        #print(response.json())
        #print("Local data")
        print(deviceData)
    else:
        print("Error getting respose")


def connectToDB():
    print('connecting to DB')

def insertInDB():
    print('to be added')

connectToDB()

def allHostsData():
    with open('data/nodes.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ip = row['ip']
            port = row['port']
            #print(row['ip'], row['port'])
            #print(row)
            collectDataWithAPI(ip, port)
            insertInDB()
















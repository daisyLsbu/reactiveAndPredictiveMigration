import requests

def testgetAPI():
    #api_url = "http://" + ip + ':' + str(port) + "/DeviceData"
    api_url = "http://localhost:5000/"
    response = requests.get(api_url)
    #response = requests.post('https://api.example.com/submit', data=data)

    print(response.status_code )
    if(response.status_code == 200):
        print(response)
    else:
        print("Error getting respose")

def testPostAPI():
    api_url = "http://localhost:5000/rttData"
    data = {'hosts' : '192.168.100.2'}
    response = requests.post(api_url, json={
  "hosts": ['18.00', '192.0.3.4', '111', '123.9', '123']
})

    print(response.status_code )
    if(response.status_code == 200):
        print(response)
    else:
        print("Error getting respose")

if __name__ == '__main__':
    print("testAPI")
    testgetAPI()
    testPostAPI()
    
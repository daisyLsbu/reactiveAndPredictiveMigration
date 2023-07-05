from flask import Flask
import psutilApp  
import json

app = Flask(__name__)

welcomeText = 'welcome to Home page'
portnum = 5001

@app.route('/')
def defaultpath():
   return welcomeText 

@app.get("/DeviceData")
def get_deviceData():
   deviceData1 = psutilApp.getCPUData()
   deviceData2 = psutilApp.getMemoryData()
   deviceData3 = psutilApp.getStorageData()
   deviceData4 = psutilApp.getNetworkData()
   
   merged = dict()

   merged.update(deviceData1)
   merged.update(deviceData2)
   merged.update(deviceData3)
   merged.update(deviceData4)
   return json.dumps(merged)

"""""
@app.get("/example")
def get_exampleData():
    countries = [
    {"id": 1, "name": "Thailand", "capital": "Bangkok", "area": 513120},
    {"id": 2, "name": "Australia", "capital": "Canberra", "area": 7617930},
    {"id": 3, "name": "Egypt", "capital": "Cairo", "area": 1010408},
      ]
    return jsonify(countries)
"""

if __name__ == '__main__':
   #app.run()
   #app.run(host='0.0.0.0')
   app.run(host="0.0.0.0", port=portnum)
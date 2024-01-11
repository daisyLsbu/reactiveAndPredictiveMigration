'''
This is a webapplication exposing 4 APIs to get the system telemetry data.
It is developed in flask using python library.
The application uses RESTful API design principles and follows CRUD operations for resources.
APIs: devicedetails, containers, combined, rttData
the port number can be provided as argument, by default it will be 5002
'''

from flask import Flask, request, jsonify
import psutilThread 
import dockerStat
import rtt
import sys

app = Flask(__name__)

welcomeText = 'welcome to Home page'  #default message
port_num = 5002 #default port number


'''
@api GET /
Home Page of the Application
'''
@app.route('/')
def defaultpath():
   return welcomeText 

'''
@api GET /devicedetails
system usage related details  
'''
@app.get("/devicedetails")
def get_deviceDetails():
   result = psutilThread.startThreads()
   return result

'''
@api GET /containers
system usage related details for all the containers
'''
@app.get("/containers")
def get_containersDetails():
   result = dockerStat.dockerstatinfo()
   return result

'''
@api GET /combined
system usage related details of device and all the containers
'''
@app.get("/combined")
def get_combineddata():
    result = psutilThread.startThreads()
    result['containers'] = dockerStat.dockerstatinfo()
    return result

'''
@api POST /combined
rtt data of this device to all the hosts provided
'''
@app.route('/rttData', methods=['POST'])
def rttData_json():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Check if the JSON data is valid
        if data is None:
            return jsonify({'error': 'Invalid JSON data'}), 400

        # Process the JSON data here (you can customize this part)
        hosts = data["hosts"]
        result = rtt.ping_host(hosts)
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
   port_num = int(sys.argv[1])
   app.run(host="0.0.0.0", port=port_num)

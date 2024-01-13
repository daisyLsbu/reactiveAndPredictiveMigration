"""
This is a webapplication exposing 4 APIs to get the system telemetry data.
It is developed in flask using python library.
The application uses RESTful API design principles and follows CRUD operations for resources.
APIs: devicedetails, containers, combined, rttData
To run this server you need Python installed on your machine.
You also need Flask module which can be installed via pip install flask command.
Then simply execute the script from terminal or cmd with optional port number argument like :
python app.py 8081
"""

from flask import Flask, request, jsonify
import psutilThread 
import dockerStat
import rtt
import sys

app = Flask(__name__)

welcomeText = 'welcome to Home page'  #default message
port_num = 5002 #default port number

@app.route('/')
def defaultpath():
   """
   Default path of the homepage which returns welcome text
   """
   return welcomeText 

@app.get("/devicedetails")
def get_deviceDetails():
   """
   Get System Details
   This api returns JSON object containing CPU utilization , Memory Utilization and Disk Utilization information.
   This api returns the following details about the device on which this app is running
   """
   result = psutilThread.startThreads()
   return result

@app.get("/containers")
def get_containersDetails():
   """
   This API returns a dictionary containing information about each running container on the system. The keys in this
   This API returns a list of dictionaries containing container information.
   """
   result = dockerStat.dockerstatinfo()
   return result

@app.get("/combined")
def get_combineddata():
    """
    This API returns system usage information about both the host machine and each Docker container running on it.
    This API returns a dictionary containing system usage information about the host machine, including CPU utilization,
    This API returns system usage data of both Device and Docker Containers combined.
    """
    result = psutilThread.startThreads()
    result['containers'] = dockerStat.dockerstatinfo()
    return result

@app.route('/rttData', methods=['POST'])
def rttData_json():
    """
    This API is used by the client application to send RTT Data to server, so that it
    can be compared with other devices.
    It takes JSON as input.
    """
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
   """
   Run Flask app on port 8081 or given port
   """
   port_num = int(sys.argv[1])
   app.run(host="0.0.0.0", port=port_num)

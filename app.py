from flask import Flask, request, jsonify
import psutilThread 
import dockerStat
import rtt
import sys

app = Flask(__name__)

welcomeText = 'welcome to Home page'
port_num = 5002

@app.route('/')
def defaultpath():
   return welcomeText 

@app.get("/devicedetails")
def get_deviceDetails():
   result = psutilThread.startThreads()
   return result

@app.get("/containers")
def get_containersDetails():
   result = dockerStat.dockerstatinfo()
   return result

@app.get("/combined")
def get_combineddata():
    result = psutilThread.startThreads()
    result['containers'] = dockerStat.dockerstatinfo()
    return result

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

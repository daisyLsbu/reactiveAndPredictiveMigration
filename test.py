import pandas as pd
import requests
import connectRemote
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def defaultpath():
   return "welcomeText" 

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
        #result = rtt.ping_host(hosts)
        print(hosts)
        result = hosts
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("test")
    app.run(host="0.0.0.0", port=5000)

  

  
'''
testing json file : create, read and write
append and update, delete
'''
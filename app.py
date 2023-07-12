from flask import Flask
import psutilThread 
import sys

app = Flask(__name__)

welcomeText = 'welcome to Home page'
port_num = 5001

@app.route('/')
def defaultpath():
   return welcomeText 

@app.get("/devicedetails")
def get_deviceDetails():
   result = psutilThread.startThreads()
   return result

if __name__ == '__main__':
   port_num = int(sys.argv[1])
   app.run(host="0.0.0.0", port=port_num)
#create a basic website using HTML, it can be used to test the data from hosts before connecting to DB
# step1: install live server and add the html file to the live server, use browser at local host to view
# step2: open html with live server
#pythonworking;, reading host lists;, fetch, async, display; display as tabular format; updates the browser automatically

import pandas as pd
import aiohttp
import asyncio
from pprint import PrettyPrinter

template_header = """ <!DOCTYPE html>
                      <html lang="en">
                      <head>
                      <meta charset="UTF-8">
                      <meta name="viewport" content="width=device-width, initial-scale=1.0">
                      <title>Document</title>
                      <h1>test</h1>
                      </head>
                      <body>"""

template_trailer = """
    </body>
    </html>"""


async def fetch(session, url):
    """Requests async requests to fetch util data from Telemetry client
    Args:
        url (str): client api endpoint
    """
    try:
        async with session.get(url) as response:
            data = await response.json()
            return data
    except:
        print(f'URL: {url} not reachable !! ')

def read_hosts():

    hosts = pd.read_csv('data/nodes.csv').transpose().to_dict()  # read csv into dictionary

    client_endpoint =[f'http://{hosts[key]["ip"]}:{hosts[key]["port"]}/{hosts[key]["api"]}'
                      for key in hosts] # list of client urls

    return client_endpoint

async def displayData(interval:int):

    pp = PrettyPrinter(indent=2)
    client_endpoints = read_hosts()  # gets list of url to clients

    async with aiohttp.ClientSession() as session:
        while True:
            #create a collection of coroutines
            fetch_coroutines = [fetch(session=session, url=url) for url in client_endpoints]

            # fetch data
            data = await asyncio.gather(*fetch_coroutines)
            tab_text=""
            for entry in data:
                tab_text += "<hr>"
                tab_text+=f'<h2>{entry["host"]}</h2>'
                entry = {k:[entry[k]] for k in entry}
                html_txt=tabulate(entry,headers='keys',tablefmt='html')
                tab_text+=html_txt 
                tab_text+='<hr>'

            with open('test.html','w') as fp:
                fp.write(template_header+tab_text+template_trailer)
            await asyncio.sleep(interval)




if __name__ == '__main__':
    hosts = read_hosts()
    asyncio.run(displayData(interval=1))

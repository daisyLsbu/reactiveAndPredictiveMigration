#pythonworking;, reading host lists;, fetch, async, display
import pandas as pd
import aiohttp
import asyncio
from pprint import PrettyPrinter
from tabulate import tabulate

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
            pp.pprint(data)


            for i in data:
                print(i)
                i = {k:[i[k]] for k in i}
                x= tabulate(i,tablefmt='html')
                pp.pprint(x)

            await asyncio.sleep(interval)

if __name__ == '__main__':

    print("Hello")

    hosts = read_hosts()
    print(hosts)

    asyncio.run(displayData(interval=1))

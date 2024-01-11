'''
This application reads the hosts list from host.csv file
countinously fetches all the data from respective hosts
and stores it in Timeseries influx DB
'''
import aiohttp
import asyncio
import pandas as pd
from pprint import PrettyPrinter
import influxdbsuite

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


async def storeData(interval:int):

    pp = PrettyPrinter(indent=2)
    client_endpoints = read_hosts()  # gets list of url to clients
    bucket="telemetrydata"

    async with aiohttp.ClientSession() as session:
        while True:
            #create a collection of coroutines
            fetch_coroutines = [fetch(session=session, url=url) for url in client_endpoints]

            # fetch data
            data = await asyncio.gather(*fetch_coroutines)
            pp.pprint(data)

            influxdbsuite.writeToDBCombinedTest(data, bucket)
            await asyncio.sleep(interval)


if __name__ == '__main__':
    asyncio.run(storeData(interval=1))
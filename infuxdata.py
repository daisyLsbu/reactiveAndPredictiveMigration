from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

# InfluxDB connection parameters
url = "http://your_influxdb_host:8086"
token = "your_auth_token"
org = "your_org"
bucket = "your_bucket"

# Create a client instance
client = InfluxDBClient(url=url, token=token, org=org)

# Define the Flux query


query = f'''
    import "influxdata/influxdb/v1"
    
    data = from(bucket: "{bucket}")
      |> range(start: -1d)
      |> v1.tagValues(tag: "host")

    distinctHosts = data |> group() |> distinct(column: "host")
'''

# Run the query
result = client.query_api().query(org=org, query=query)

# Extract and print the distinct tag values
for table in result:
    for record in table.records:
        tag_value = record.values['host']
        print(tag_value)

# Close the client
client.__del__()





'''
from influxdb import InfluxDBClient

# Configure the InfluxDB connection parameters
host = "your_influxdb_host"
port = 8086
database = "your_database_name"

# Create a client instance
client = InfluxDBClient(host=host, port=port, database=database)

# Define the tag key for which you want to retrieve distinct values
tag_key = "host"

# Build and execute the SHOW TAG VALUES query
query = f'SHOW TAG VALUES ON "{database}" WITH KEY = "{tag_key}"'
result = client.query(query)

# Parse the result to get the distinct tag values
distinct_values = [row[tag_key] for row in result.get_points()]

# Print the distinct tag values
for value in distinct_values:
    print(value)

# Close the client connection
client.close()

from(bucket: "telemetryData")
	|> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn: (r) => r["_measurement"] == "test8")
  |> filter(fn: (r) => r["_field"] == "cpu")
  |> group()
  |> group(columns: ["10.35.84.126"])

  from(bucket: "telemetryData")
    |> group(columns: ["host"])
    |> distinct(column: "host")


Save to grepper
Remember to replace "your_influxdb_host", your_database_name, and ensure that your InfluxDB server is running and accessible.

Please note that the influxdb package is designed for InfluxDB v1. If you're working with InfluxDB v2 (also known as InfluxDB 2.0 or InfluxDB Cloud), you should use the InfluxDB 2.0 Python client, which is different from the influxdb package used for InfluxDB v1.
'''





import docker

def dockerstatinfo():
    client = docker.from_env()
    result = []

    for containers in client.containers.list():
        data = containers.stats(decode=None, stream = False)

        #get customised values
        containerid = containers.short_id

        # Extract CPU, memory and network utilization values
        cpu_usage = data["cpu_stats"]["cpu_usage"]["total_usage"]
        memory_usage = data["memory_stats"]["usage"]       
        nw_usage = data["networks"]["eth0"]["rx_bytes"] + data["networks"]["eth0"]["tx_bytes"]

        # Calculate utilization percentage
        cpu_utilization = (cpu_usage / data["cpu_stats"]["system_cpu_usage"]) * 100
        memory_utilization = (memory_usage / data["memory_stats"]["limit"]) * 100
        nw_utilization = (nw_usage / (1024 * 1024)) * 100  # Convert to Mbps

        stats = {"id": containerid, "cpu_usage": cpu_usage, "memory_usage": memory_usage, "nw_usage": nw_usage, "cpu_per": cpu_utilization, "mem_per": memory_utilization, "nw": nw_utilization}
        #send the stat as it is if implementing graphQL in other layer
        #result.append(data)
        #UsageDelta = data['cpu_stats']['cpu_usage']['total_usage'] - data['precpu_stats']['cpu_usage']['total_usage']

        result.append(stats)
    return result

'''
for unit testing
result_out = dockerstatinfo()
print(result_out)
'''
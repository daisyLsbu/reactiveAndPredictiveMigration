from pythonping import ping

hosts = [
    '8.8.8.8'
]
rtt_values = []
def ping_host(hosts):
    """
    Ping a list of hosts and return the round trip time (in ms) for each host
    :param hosts: List of hosts to be pinged
    :return rtt_values: A list containing the RTT values for each host
    """
    for host in hosts:
        print("Pinging %s" %(host))
        ping_result = ping(target=host, size=40, count=10) #ping(target=host, count=10000, size=1500) #
        rtt_values.append(
        {
        'host': host,
        'avg_latency': ping_result.rtt_avg_ms,
        'min_latency': ping_result.rtt_min_ms,
        'max_latency': ping_result.rtt_max_ms,
        'packet_loss': ping_result.packet_loss
        })
    return rtt_values
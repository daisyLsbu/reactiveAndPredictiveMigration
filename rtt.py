#testing ping in python 

from pythonping import ping

hosts = [
    '8.8.8.8'
]
rtt_values = []


def ping_host(hosts):
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

#print(ping_host(hosts))

'''
#worked
#ping('8.8.8.8') 
#[ping(host) for host in hosts]

#for host in hosts:
#    ping_result = ping(host)
#    print(ping_result.rtt_avg)

def ping_host(host):
    ping_result = ping(target=host, count=10, timeout=2)

    return {
        'host': host,
        'avg_latency': ping_result.rtt_avg_ms,
        'min_latency': ping_result.rtt_min_ms,
        'max_latency': ping_result.rtt_max_ms,
        'packet_loss': ping_result.packet_loss
    }

hosts = [
    '8.8.8.8'
]

for host in hosts:
    print("welcome")
    ping_host(host)
    '''
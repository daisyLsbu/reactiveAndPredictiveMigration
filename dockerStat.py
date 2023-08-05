import docker
from pprint import PrettyPrinter

def dockerstatinfo():
    pp = PrettyPrinter(indent=2)
    client = docker.from_env()
    result = []
    result_out = {}

    for containers in client.containers.list():
        containerid = containers.short_id
        stats = containers.stats(decode=None, stream = False)
        UsageDelta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']


        # from informations : UsageDelta = 25382985593 - 25382168431
        '''
        pp.pprint(containerid)
        pp.pprint(stats)
        pp.pprint(UsageDelta)
        '''
        result.append(stats)
    return result

'''
result_out = dockerstatinfo()
print(result_out)
'''
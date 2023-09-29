import paramiko
from scp import SCPClient

def sshTest():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.122.210", 22, 'ubuntu', 'ubuntu')
    ssh.exec_command('ls -l')
    ssh.exec_command('touch testssh.txt')

def sshmigrate(srcIP, id):
    """_summary_
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(srcIP, 22, 'ubuntu', 'ubuntu')
    ssh.exec_command(f'python3 migrateVictim.py {id}')

def sshrestore(destIp):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(destIp, 22, 'ubuntu', 'ubuntu')
    ssh.exec_command('python3 restoreimage.py')

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def sshcopy_(server1, server2, port, user, password):
    ssh = createSSHClient(server1, port, user, password)
    scp = SCPClient(ssh.get_transport())
    scp.get('ubuntu-test.img')
    ssh = createSSHClient(server2, port, user, password)
    scp = SCPClient(ssh.get_transport())
    scp.put('ubuntu-test.img')

def sshcopy(server1, server2, port, user, password):
    ssh = createSSHClient(server1, port, user, password)
    scp = SCPClient(ssh.get_transport())
    scp.get('/home/ubuntu/images/ubuntu-test.img')
    print("got")

    ssh = createSSHClient(server2, port, user, password)
    scp = SCPClient(ssh.get_transport())
    scp.put('ubuntu-test.img')
    ssh.exec_command('sudo mv ubuntu-test.img /home/ubuntu/images/')

if __name__ == '__main__':
    print("sshcopy")
    sshcopy('192.168.122.80', '192.168.122.210', 22, 'ubuntu', 'ubuntu')




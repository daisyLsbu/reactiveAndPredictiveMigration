import paramiko

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

#sshTest()
#docker run -d 5a81c4b8502e
#sshmigrate() 
#sshrestore()




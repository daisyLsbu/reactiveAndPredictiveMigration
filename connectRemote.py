import paramiko
"""
host = '192.168.122.77'
user = 'ubuntu'
pw = 'ubuntu'
migrationScript = 'python3 migrate.py'

ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(host, user, pw)
stdin, stdout, stderr = ssh_client.exec_command('ls -l')
#
#session = paramiko.ssh_clinet(host_name, user_name, password)
#with session.open() as s:
 #   s.cmd(migrationScript)
 """
def ssh(host, user, pw, script, id):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, 22, user, pw)
    ssh.exec_command('ls -l')
    ssh.exec_command(f'python3 {script} {id}')

def sshTest():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.122.210", 22, 'ubuntu', 'ubuntu')
    ssh.exec_command('ls -l')
    ssh.exec_command('touch testfile.txt')

sshTest()




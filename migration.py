import paramiko

host = '192.168.1.111'
user = 'user'
pw = 'password'

ssh_client = paramiko.SSHClient()
ssh_client.connect(hostname= host, username= user, password= pw)
stdin, stdout, stderr = ssh_client.exec_command('ls -l')


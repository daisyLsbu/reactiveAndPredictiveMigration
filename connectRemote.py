import paramiko

host = '192.168.1.111'
user = 'user'
pw = 'password'
migrationScript = 'python3 migrate.py'

ssh_client = paramiko.SSHClient()
ssh_client.connect(hostname= host, username= user, password= pw)
stdin, stdout, stderr = ssh_client.exec_command('ls -l')
#
#session = paramiko.ssh_clinet(host_name, user_name, password)
with session.open() as s:
    s.cmd(migrationScript)


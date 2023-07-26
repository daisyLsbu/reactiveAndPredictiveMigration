import subprocess as sbp

a = 'hello'
victim_id = '1e176f5e8bab' 
victim_name = 'ubuntu-test'
backup_path = '/home/ubuntu/images/'
backup_img = 'ubuntu-test.img'

command = f"""
            echo {a}; 
            docker --version;
            docker images;
            docker ps;
            docker commit {victim_id}  {victim_name};
            docker images;
            docker ps -a;
            docker ps;
            docker save -o {backup_path}{backup_img} {victim_name};
            docker ps;
            docker stop {victim_id};
            docker ps;
            docker rm {victim_id};
            cd {backup_path};
            ls -lrt;
            docker rmi {victim_name};
            """
# scp and delete file
ret = sbp.run(command, capture_output=True, shell=True)
print(ret.stdout.decode())

""""" use later
            docker commit {victim_id}  {victim_name}
            docker images
            docker ps -a 
            docker ps
            docker save -o {backup_path} {victim_name}
            docker ps
            docker stop {victim_id}
"""


#a = 'hello'
#command = f"""echo {a}; 
#            echo b; 
#            ls; 
#            pwd"""
#ret = sbp.run(command, capture_output=True, shell=True)
#print(ret.stdout.decode())

#command = "echo a; echo b; ls; pwd"
#ret = sbp.run(command, capture_output=True, shell=True)
#print(ret.stdout.decode())

#cmd = "ls"
#sbp.run([cmd])

#sbp.run(["ls"])
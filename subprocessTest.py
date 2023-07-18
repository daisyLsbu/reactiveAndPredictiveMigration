import subprocess as sbp

a = 'hello'
victim_id = 'c404f4f952b0' 
victim_name = 'test_img_4'
backup_path = 'data/'
backup_img = 'test_img4.img'

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
            pwd
            """

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
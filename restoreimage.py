import subprocess as sbp

a = 'hello'
image_name = 'ubuntu-test:latest'
image_path = '/home/user/images/ubuntu-test.img'

command = f"""
            echo {a}; 
            docker --version;
            docker images;
            docker ps;
            docker load -i {image_path};
            docker images;
            docker run -it {image_name};            
            docker images;
            docker ps -a;
            docker ps;
            pwd
            """

ret = sbp.run(command, capture_output=True, shell=True)
print(ret.stdout.decode())

#docker load -i /Users/daisy/Desktop/test_img.img
#            docker run -it test_img:latest


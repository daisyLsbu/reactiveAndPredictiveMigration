# at the node migrate.py
#import subprocess as sbp

#victim = get_victim()
#image_name = get_image_name(victim)
#target = get_target()

cmd = f"""
    docker images
    docker ps
    docker commit 44638ac4512e  test_img
    docker images
    docker ps -a 
    docker ps
    docker save -o Desktop/test_img.img test_img
    docker ps
    docker stop 44638ac4512e
    docker ps
    """

print(cmd)

def helper():
    return cmd

helper()

#sbp.popen([cmd])
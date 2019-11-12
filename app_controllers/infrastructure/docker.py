import subprocess
from subprocess import check_output

def dockerGetContainerId(podId):
    command = ["kubectl","describe","pod",podId]
    command_output = check_output(command).split()
    container_id = ''
    for i in command_output:
        # print(i)
        if 'docker://' in str(i):
            container_id = i.decode("utf-8").replace('\'','').split("docker://",1)[1]
            print("FOUND CONTAINER_ID:",container_id)
    return container_id
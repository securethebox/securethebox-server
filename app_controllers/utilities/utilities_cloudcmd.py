import subprocess
from subprocess import check_output
from ..infrastructure.kubernetes import (
    kubernetesGetPodId
)
from ..infrastructure.docker import (
    dockerGetContainerId
)

# Install Cloudcmd on Container/Pod
def utilitiesSetupCloudcmd(clusterName, serviceName, userName):
    print("setupCLOUDCMD!!!",clusterName,serviceName,userName)

    pod_id = kubernetesGetPodId(serviceName,userName)
    container_id = dockerGetContainerId(pod_id)

    if serviceName == 'nginx-modsecurity':
        subprocess.Popen([f"docker exec -u root "+container_id+" apk add nodejs nodejs-npm"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" npm install -g cloudcmd forever"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" forever start /usr/bin/cloudcmd --port 9000"],shell=True).wait()
    
    elif serviceName == 'juice-shop':
        subprocess.Popen([f"docker exec -u root "+container_id+" npm install -g cloudcmd forever"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" forever start /usr/local/bin/cloudcmd --port 9000"],shell=True).wait()

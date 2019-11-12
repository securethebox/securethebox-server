import subprocess
from subprocess import check_output
import requests
import json
from ..infrastructure.kubernetes import (
    kubernetesGetPodId
)
from ..infrastructure.docker import (
    dockerGetContainerId
)

"""
Start this script

"""

def attackerSetupKaliLinux(clusterName,serviceName,userName):
    print("SETUP ATTACKER",clusterName,serviceName,userName)
    subprocess.Popen([f"kubectl apply -f ./kubernetes-deployments/pods/kali-linux/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    
    # copy python script file
    pod_id = kubernetesGetPodId(serviceName,userName)
    container_id = dockerGetContainerId(pod_id)
    subprocess.Popen([f"docker cp ./kubernetes-deployments/pods/kali-linux/exploit_1_generate_payload.py "+container_id[:12]+":/root"],shell=True).wait()
    
    # check if last line in log is 'done'

    # setup shell listener on metasploit

    # should have a shell

    # execute remote command to start shutdown apis

    # subprocess.Popen([f"kubectl delete -f ./kubernetes-deployments/pods/kali-linux/01_pod.yml"],shell=True).wait()
    # kubernetesGenerateServicesYaml("us-west1-a", 'kali-linux','charles')
    # kubernetesManageServicesPod("us-west1-a",'kali-linux', 'charles', 'apply')
    # kubernetesManageServicesPod("us-west1-a",'kali-linux', 'charles', 'delete')
    # kubernetesDeleteServicesYaml("us-west1-a",'kali-linux','charles')
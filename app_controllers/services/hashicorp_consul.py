import subprocess
from subprocess import check_output

"""
Need consul to start this script

"""
def hashicorpConsulDeploy():
    command = ["consul","keygen"]
    command_output = check_output(command).split()
    gossip_encryption_key = command_output[0].decode("utf-8")

    subprocess.Popen([f"kubectl create secret generic consul \
        --from-literal=\"gossip-encryption-key="+gossip_encryption_key+"\" \
        --from-file=./kubernetes-deployments/services/hashicorp-consul/ca.pem \
        --from-file=./kubernetes-deployments/services/hashicorp-consul/consul.pem \
        --from-file=./kubernetes-deployments/services/hashicorp-consul/consul-key.pem"],shell=True).wait()    
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-consul/_01_config.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-consul/_02_service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-consul/_03_statefulset.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl create -f ./kubernetes-deployments/services/hashicorp-consul/_04_ingress.yml"],shell=True).wait()

if __name__ == "__main__":
    hashicorpConsulDeploy()
import subprocess
import json
import os 
from subprocess import check_output


def kubernetesGetPodId(serviceName, userName):
    command = ["kubectl","get","pods","-o","go-template","--template","'{{range .items}}{{.metadata.name}}{{\"\\n\"}}{{end}}'"]
    # Command Output
    out = check_output(command)
    # List of online pods into a List
    pod_list = out.decode("utf-8").replace('\'','').splitlines()

    pod_id = ''
    findPod = True
    counter = 0
    while findPod:
        if counter > 10:
            findPod=False
        print(f"Setup {serviceName} counter:",counter)
        for i in pod_list:
            if f'{serviceName}-{userName}' in str(i):
                pod_id = str(i)
                findPod=False
                print("FOUND POD_ID:",pod_id)
        counter+=1
    return pod_id


def kubernetesGetPodStatus(podId):
    command = ["kubectl","get","pod",podId,"-o","json"]
    command_output = check_output(command)
    parsedJSON = json.loads(command_output)
    currentState = parsedJSON["status"]["containerStatuses"][0]["state"]
    # print(parsedJSON["status"]["containerStatuses"][0]["state"])
    for i in currentState:
        print("Key:",i)
        if i == "running":
            return True
        elif i != "running":
            return False


def kubernetesGenerateIngressYaml(clusterName,serviceName):
    print("Generating Ingress Yaml",clusterName,serviceName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/01_permissions.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/02_cluster-role.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/03_config.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/04_deployment.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/05_service.py {clusterName} {serviceName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/ingress/{serviceName}/06_ingress.py {clusterName} {serviceName}"],shell=True).wait()

def kubernetesGeneratePodsYaml(clusterName,serviceName,userName):
    print("Generating Pod Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/pods/{serviceName}/01_deployment.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def kubernetesGenerateServicesYaml(clusterName, serviceName, userName):
    print("Generating Service Yaml",clusterName,serviceName,userName)
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/01_deployment.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/02_service.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/{serviceName}/03_ingress.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def kubernetesDeleteIngressYaml(clusterName, serviceName):
    print("Deleting Ingress Yaml")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def kubernetesDeleteServicesYaml(clusterName,serviceName, userName):
    print("Deleting Service Yaml")
    # print(f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()

def kubernetesManageIngressPod(clusterName,serviceName, action):
    print(action,"Ingress Pod:",serviceName)
    # print(f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml")
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/01_{clusterName}-{serviceName}-permissions.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/02_{clusterName}-{serviceName}-cluster-role.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/03_{clusterName}-{serviceName}-config.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/04_{clusterName}-{serviceName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/05_{clusterName}-{serviceName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/ingress/{serviceName}/06_{clusterName}-{serviceName}-ingress.yml"],shell=True).wait()

def kubernetesCreatePersistentVolumes(action):
    print('Creating Persistent Volume and Claim')
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    # kubectl apply -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml
    # kubectl apply -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml

def kubernetesManagePods(clusterName, serviceName, userName, action):
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/pods/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()

def kubernetesManageServicesPod(clusterName, serviceName, userName, action):
    print(action,"Service Pod:",serviceName)
    if action == 'apply':
        print('Creating Persistent Volume and Claim')
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True).wait()
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/01_{clusterName}-{serviceName}-{userName}-deployment.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/02_{clusterName}-{serviceName}-{userName}-service.yml"],shell=True).wait()
    subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/services/{serviceName}/03_{clusterName}-{serviceName}-{userName}-ingress.yml"],shell=True).wait()


if __name__ == "__main__":
    kubernetesGetPodId('jenkins','charles')
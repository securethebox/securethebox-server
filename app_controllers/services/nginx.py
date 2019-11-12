import subprocess
from subprocess import check_output

def nginxGenerateConfig(clusterName,serviceName,userName):
    print("Generating Nginx Config")
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py {clusterName} {serviceName} {userName}"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

def nginxDeleteConfig(clusterName,serviceName,userName):
    print("Deleting Nginx Config")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx-2.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-modsecurity.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

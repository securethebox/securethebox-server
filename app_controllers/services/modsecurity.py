import subprocess
from subprocess import check_output
import time
from ..services.nginx import (
    nginxGenerateConfig,
    nginxDeleteConfig,
)

# Install Nginx on Container/Pod
def modsecuritySetup(clusterName, serviceName, userName):
    print("Checking if Service up with GET request")
    try:
        response = requests.request("GET", 'http://nginx-modsecurity-charles.us-west1-a.securethebox.us')
        print(response.text)
    except:
        print("Cannot get response...")
    print("Setup WAF for:",serviceName,userName)
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
        print("Setup WAF counter:",counter)
        for i in pod_list:
            if f'nginx-modsecurity-{userName}' in str(i):
                print("FOUND POD_ID:",str(i))
                pod_id = str(i)
                findPod=False
        counter+=1
        
    nginxGenerateConfig(clusterName,serviceName,userName)
    print("POD_ID:",pod_id)
    print("modsecuritySetup - Sleeping 10 seconds for nginx service to load...")
    time.sleep(10)
    try:
        print("Copying nginx file to Pod")
        subprocess.Popen([f"kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-nginx-2.conf "+pod_id+":/etc/nginx/nginx.conf"],shell=True).wait()
        subprocess.Popen([f"kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/04_{clusterName}-{serviceName}-{userName}-modsecurity.conf "+pod_id+":/etc/nginx/modsec/modsecurity.conf"],shell=True).wait()
        print("Confirming nginx.conf and modsecurity.conf file copied...")
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- cat /etc/nginx/nginx.conf | grep "+serviceName+""],shell=True).wait()
        print("Reloading Nginx service")
        subprocess.Popen([f"kubectl exec -it "+pod_id+" -- nginx -s reload"],shell=True).wait()
        print("Checking output of reloading Nginx:")
        nginxReloadCommand = ["kubectl","exec","-it",pod_id,"--", "nginx", "-s", "reload"]
        try:
            nginxReloadOut = check_output(nginxReloadCommand)
            print("Reload Output:",nginxReloadOut.decode("utf-8"))
            print("Deleting Nginx Conf File...")
            nginxDeleteConfig(clusterName,"juice-shop",userName)
            print("COMPLETE!!!!")
        except:
            print("Error occured... on nginxReloadOut...")
            modsecuritySetup(clusterName, serviceName, userName)    
        
    except: 
        print("Error occured... retrying modsecuritySetup...")
        modsecuritySetup(clusterName, serviceName, userName)    
    # kubectl exec -it splunk-oppa-75fff68596-jbq46 -- /bin/sh
    # kubectl cp ./kubernetes-deployments/services/nginx-modsecurity/nginx.conf nginx-modsecurity-oppa-6b7f54ff8-fszg6:/etc/nginx/nginx.conf

import subprocess
from subprocess import check_output
import time
from ..infrastructure.kubernetes import (
    kubernetesGetPodId
)
from ..infrastructure.docker import (
    dockerGetContainerId
)

def splunkUniversalForwarderGenerateConfig(clusterName,serviceName,userName):
    print("Generating Splunk Config")
    subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/splunk-universal-forwarder/04_configuration.py {clusterName} {serviceName} {userName}"],shell=True).wait()

def splunkUniversalForwarderDeleteConfig(clusterName,serviceName,userName):
    print("Deleting Splunk Universal Forwarder Config")
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-2.conf"],shell=True).wait()
    subprocess.Popen([f"rm -rf ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-3.conf"],shell=True).wait()
    # python3.7 ./kubernetes-deployments/services/nginx-modsecurity/04_configuration.py us-west1-a nginx-modsecurity oppa

def splunkSetupUserPreferences(container_id):
    # doc
    # /opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf
    # tz = America/Los_Angeles
    # docker exec -it 0f0b570de296 /bin/sh
    # need to login as admin first
    print("Setting up Splunk User Preferences",container_id[:12])
    try:
        subprocess.Popen([f"python3.7 ./kubernetes-deployments/services/splunk/check_login.py"],shell=True).wait()
        # mkdir -p /opt/splunk/etc/users/admin/user-prefs/local/
        subprocess.Popen([f"docker exec -u root "+container_id+" mkdir -p /opt/splunk/etc/users/admin/user-prefs/local/"],shell=True).wait()
        subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/user-prefs.conf "+container_id[:12]+":/opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" cat /opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunk/bin/splunk restart"],shell=True).wait()
    except:
        print("Trying again...")
        splunkSetupUserPreferences(container_id)

    # docker cp ./kubernetes-deployments/services/splunk/user-prefs.conf 24d56f0c7156:/opt/splunk/etc/users/admin/user-prefs/local/user-prefs.conf

def splunkSetupPortForwarding(userName):
    pod_id = kubernetesGetPodId("splunk",userName)
    subprocess.Popen([f"kubectl port-forward "+pod_id+" 8000:8000"],shell=True).wait()
    # kubectl port-forward splunk-charles-c76dd785b-f6z5l 8000:8000
    # kubectl port-forward wazuh-elasticsearch-0 9200:9200
    # os.spawnl(os.P_DETACH, "kubectl port-forward "+pod_id+" 8000:8000")
    # subprocess.Popen([f"kubectl port-forward "+pod_id+" 8089:8089"],shell=True).wait()

def splunkSetupAddons(clusterName,serviceName,userName):
    print("Setting up splunk addons")
    pod_id = kubernetesGetPodId("splunk",userName)
    
    # 2. get container_id
    container_id = dockerGetContainerId(pod_id)
    # 3. Copy inputs
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/modsecurity-add-on-for-splunk.tgz "+container_id+":/opt/splunk/etc/apps/"],shell=True).wait()
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/suricata-add-on-for-splunk.tgz "+container_id+":/opt/splunk/etc/apps/"],shell=True).wait()
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk/wazuh-add-on-for-splunk.tgz "+container_id+":/opt/splunk/etc/apps/"],shell=True).wait()
    # Unpack tgz addon
    subprocess.Popen([f"docker exec -u root "+container_id+" tar xvzf /opt/splunk/etc/apps/modsecurity-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
    subprocess.Popen([f"docker exec -u root "+container_id+" tar xvzf /opt/splunk/etc/apps/suricata-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
    subprocess.Popen([f"docker exec -u root "+container_id+" tar xvzf /opt/splunk/etc/apps/wazuh-add-on-for-splunk.tgz -C /opt/splunk/etc/apps"],shell=True).wait()
    # Restart splunk service
    subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunk/bin/splunk restart"],shell=True).wait()

# # Setup Addons
#     splunkSetupSplunkAddons(clusterName,serviceName,userName)
#     # Setup User Preferences
#     splunkSetupUserPreferences(container_id)

def splunkSetupMasterServer(clusterName, userName):
    print("Setting up Splunk Master Setup")
    # 1. get splunk-universal-forwarder pod_id
    pod_id = kubernetesGetPodId("splunk",userName)
    
    # 2. get container_id
    container_id = dockerGetContainerId(pod_id)
    splunkSetupAddons(clusterName,"splunk",userName)
    splunkSetupUserPreferences(container_id)
    splunkSetupPortForwarding(userName)

def splunkSetupForwarderLogging(clusterName,serviceName,userName):
    """
    0. enable splunk receving
    1. get splunk-universal-forwarder pod_id
    2. get container_id
    3. Run copy inputs over to container
    4. Add Splunk server to forward logs
    5. Restart splunk-universal-forwarder service

    kubectl describe pod splunk-universal-forwarder-oppa-747d54cb-wtlzg
    docker exec -u root 4c35ca0d76dccc84e93896d7c953da8bb119c08fbd4af50dc7842682198a41ef whoami
    """

    splunkUniversalForwarderGenerateConfig(clusterName,serviceName,userName)
    print("Sleeping 30 Seconds for splunk to get ready")
    time.sleep(30)

    # 1. get splunk-universal-forwarder pod_id
    pod_id = kubernetesGetPodId("splunk-universal-forwarder",userName)
    
    # 2. get container_id
    container_id = dockerGetContainerId(pod_id)
    
    # 3. Copy inputs
    subprocess.Popen([f"docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-2.conf "+container_id+":/opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
    # docker cp ./kubernetes-deployments/services/splunk-universal-forwarder/04_us-west1-a-splunk-universal-forwarder-oppa-inputs.conf 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc:/opt/splunkforwarder/etc/system/local/inputs.conf
    # Check file is copied
    subprocess.Popen([f"docker exec -u root "+container_id+" cat /opt/splunkforwarder/etc/system/local/inputs.conf"],shell=True).wait()
    # docker exec -u root 482a82302dfbc874d6baae8c12066c6bcc73ba25d8bda506f435ee1f942d96fc cat /opt/splunkforwarder/etc/system/local/inputs.conf
    
    try:
        # 4. point Universal forwarder to splunk server
        # This command should show a FATAL error, its supposed to happend in order for splunk to login
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk search 'index=_internal | fields _time | head 1 ' -auth 'admin:Changeme'"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk add forward-server splunk-"+userName+":9997"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/nginx-"+userName+".log"],shell=True).wait()
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk add monitor /var/log/challenge1/modsecurity-"+userName+".log"],shell=True).wait()

        # 5. Restart splunk-universal-forwarder service
        subprocess.Popen([f"docker exec -u root "+container_id+" /opt/splunkforwarder/bin/splunk restart"],shell=True).wait()
        
        # 6. Clean up inputs files on host
        splunkUniversalForwarderDeleteConfig(clusterName,"splunk-universal-forwarder",userName)
    except:
        print("Failed to setup Splunk Forwarder... retrying in 10 seconds")
        time.sleep(10)
        splunkSetupForwarderLogging(clusterName,serviceName,userName)

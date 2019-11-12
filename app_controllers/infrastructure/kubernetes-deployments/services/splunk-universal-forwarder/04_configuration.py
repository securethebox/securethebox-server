import sys
from shutil import copyfile
import subprocess

def writeConfig(clusterName,serviceName,userName):
    # Copy Template file
    copyfile('./kubernetes-deployments/services/splunk-universal-forwarder/template-inputs.conf', './kubernetes-deployments/services/splunk-universal-forwarder/04_'+str(sys.argv[1])+'-'+str(sys.argv[2])+'-'+str(sys.argv[3])+'-inputs.conf')
    # Replace Line in file
    subprocess.Popen([f"sed '2s/nginx-userName/nginx-{userName}/' './kubernetes-deployments/services/splunk-universal-forwarder/template-inputs.conf' > ./kubernetes-deployments/services/splunk-universal-forwarder/04_"+str(sys.argv[1])+"-"+str(sys.argv[2])+"-"+str(sys.argv[3])+"-inputs.conf"],shell=True).wait()
    subprocess.Popen([f"sed '5s/modsecurity-userName/modsecurity-{userName}/' './kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs.conf' > ./kubernetes-deployments/services/splunk-universal-forwarder/04_"+str(sys.argv[1])+"-"+str(sys.argv[2])+"-"+str(sys.argv[3])+"-inputs-2.conf"],shell=True).wait()
    subprocess.Popen([f"sed '8s/suricata-userName/suricata-{userName}/' './kubernetes-deployments/services/splunk-universal-forwarder/04_{clusterName}-{serviceName}-{userName}-inputs-2.conf' > ./kubernetes-deployments/services/splunk-universal-forwarder/04_"+str(sys.argv[1])+"-"+str(sys.argv[2])+"-"+str(sys.argv[3])+"-inputs-3.conf"],shell=True).wait()

# usage:    
if __name__ == "__main__":
  writeConfig(clusterName=str(sys.argv[1]),serviceName=str(sys.argv[2]),userName=str(sys.argv[3]))
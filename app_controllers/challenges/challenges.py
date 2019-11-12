import subprocess
from subprocess import check_output
import time
import os 
from ..services.gitlab import (
    gitlabGetResetPasswordToken, 
    gitlabPostResetPassword,
    gitlabCreatePersonalAccessToken,
    gitlabCreateProject,
    gitlabMakeProjectPublic,
    gitlabProjectAddDeployKey,
    gitlabProjectAddWebhook,
    gitlabProjectAllowOutbound,
    gitlabProjectAddDeployKey
)
from ..services.jenkins import (
    jenkinsConnectGitlab,
    jenkinsCreateJob,
    jenkinsCreateSSHKeypair,
    jenkinsCredentialsAddSSHPrivateKey,
    jenkinsGetSSHPrivateKey,
    jenkinsGetSSHPublicKey,
    jenkinsInstallPlugin,
    jenkinsJobAddSourceCodeManagement,
    jenkinsRestartServer
)
from ..infrastructure.docker import (
    dockerGetContainerId
)
from ..infrastructure.kubernetes import (
    kubernetesGetPodId,
    kubernetesGetPodStatus,
    kubernetesGenerateIngressYaml,
    kubernetesGeneratePodsYaml,
    kubernetesGenerateServicesYaml,
    kubernetesDeleteIngressYaml,
    kubernetesDeleteServicesYaml,
    kubernetesManageIngressPod,
    kubernetesCreatePersistentVolumes,
    kubernetesManagePods,
    kubernetesManageServicesPod,   
)
from ..services.nginx import (
    nginxGenerateConfig,   
)
from ..services.modsecurity import (
    modsecuritySetup
)
from ..services.splunk import (
    splunkUniversalForwarderGenerateConfig,
    splunkUniversalForwarderDeleteConfig,
    splunkSetupUserPreferences,
    splunkSetupMasterServer,
    splunkSetupPortForwarding,
    splunkSetupAddons,
    splunkSetupForwarderLogging,
)
from ..red_team.attacker_kali_linux import (
    attackerSetupKaliLinux
)
from ..utilities.utilities_cloudcmd import (
    utilitiesSetupCloudcmd
)

def challengesManageChallenge1(clusterName, userName, action):
    print(action,"Challenge 1",clusterName,userName)
    if action == 'apply':
        print("cwd:",os.getcwd())
        currentPath  = os.getcwd()
        os.chdir(currentPath+'/app_controllers/infrastructure')
        print("cwd:",os.getcwd())
        
        # start = time.time()
        # # 1. Generate Yaml Ingress Files
        kubernetesGenerateIngressYaml(clusterName, 'traefik')
        # # 2. Deploy Ingress Pods
        kubernetesManageIngressPod(clusterName, 'traefik', action)
        # # 3. Generate Yaml Service Files
        # time.sleep(10)
        # # SETUP GITLAB
        # kubernetesGenerateServicesYaml(clusterName, 'gitlab',userName)
        # kubernetesManageServicesPod(clusterName,'gitlab',userName, action)
        # kubernetesGenerateServicesYaml(clusterName, 'jenkins',userName)
        # kubernetesManageServicesPod(clusterName,'jenkins',userName, action)
        # print("Sleeping 100 seconds")
        # time.sleep(100)
        # print("Finished sleeping ...")
        # reset_token,session_cookie = gitlabGetResetPasswordToken(clusterName,userName)
        # gitlabPostResetPassword(reset_token,session_cookie,clusterName,userName)
        # gitlabCreateProject(clusterName, userName)
        # gitlabMakeProjectPublic(clusterName, userName)
        # gitlabProjectAllowOutbound(clusterName, userName)
        # gitlabProjectAddWebhook(clusterName, userName)
        # # SETUP APP SERVER
        # os.chdir('..')
        # os.chdir('..')
        # print("---------------------------CWD:",os.getcwd())
        # kubernetesGenerateServicesYaml(clusterName, 'juice-shop',userName)
        # kubernetesManageServicesPod(clusterName,'juice-shop', userName, action)
        # # wait for app to fully deploy
        # # time.sleep(120)
        # # SETUP JENKINS
        # jenkinsInstallPlugin("us-west1-a",userName)
        # print("Plugin Installed")
        # time.sleep(30)
        # api_token = gitlabCreatePersonalAccessToken()
        # print("API TOKEN:",api_token)
        # jenkinsConnectGitlab(api_token,"us-west1-a",userName)
        # time.sleep(30)
        # jenkinsRestartServer("us-west1-a",userName)
        # print("DONE")
        # time.sleep(30)
        # jenkinsCreateSSHKeypair('jenkins',userName)
        # jenkinsCreateJob('jenkins',userName)
        # public_key = jenkinsGetSSHPublicKey('jenkins',userName)
        # gitlabProjectAddDeployKey(public_key,clusterName,userName)
        # end = time.time()
        # print("EVERYTHING SHOULD BE DONE! Time elapsed:",end - start)

        
        

        kubernetesGenerateServicesYaml(clusterName, 'nginx-modsecurity',userName)
        
        # kubernetesGenerateServicesYaml(clusterName, 'splunk',userName)
        # kubernetesGenerateServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
        
        # # kubernetesGeneratePodsYaml(clusterName, 'kali-linux',userName)
        # # 4. Deploy Service pods
        kubernetesManageServicesPod(clusterName,'nginx-modsecurity', userName, action)
        
        # kubernetesManageServicesPod(clusterName,'splunk', userName, action)
        # kubernetesManageServicesPod(clusterName,'splunk-universal-forwarder',userName, action)
        
        # # kubernetesManagePods(clusterName,'kali-linux',userName, action)
        # # kubernetesManageServicesPod(clusterName,'wireshark',userName, action)

        # print("WAF setup")
        # modsecuritySetup(clusterName, 'juice-shop', userName)
        
        # print("Splunk Universal Forwarder Setup")
        # splunkSetupForwarderLogging(clusterName, 'splunk-universal-forwarder', userName)

        # # Setup Cloudcmd
        # print("Cloudcmd Setup")
        # setupCLOUDCMD(clusterName, 'nginx-modsecurity', userName)
        # setupCLOUDCMD(clusterName, 'juice-shop', userName)

        # # Setup Attacker
        # setupAttacker(clusterName,'kali-linux',userName)

        # Setup Port Forwarding
        # splunkSetupMasterServer(clusterName,userName)
        

    elif action == 'delete':
        # 1. Delete Ingress Pods
        kubernetesManageIngressPod(clusterName,'traefik', action)
        # 2. Generate Yaml Ingress Files
        kubernetesDeleteIngressYaml(clusterName,'traefik')
        # 3. Delete Service Pods
        kubernetesManageServicesPod(clusterName, 'nginx-modsecurity',userName, action)
        kubernetesManageServicesPod(clusterName, 'juice-shop', userName, action)
        kubernetesManageServicesPod(clusterName, 'splunk', userName, action)
        kubernetesManageServicesPod(clusterName, 'splunk-universal-forwarder', userName, action)
        kubernetesManageServicesPod(clusterName, 'jenkins', userName, action)
        kubernetesManageServicesPod(clusterName, 'gitlab', userName, action)
        # 4. Delete Yaml Files
        kubernetesDeleteServicesYaml(clusterName, 'nginx-modsecurity',userName)
        kubernetesDeleteServicesYaml(clusterName, 'juice-shop',userName)
        kubernetesDeleteServicesYaml(clusterName, 'splunk',userName)
        kubernetesDeleteServicesYaml(clusterName, 'splunk-universal-forwarder',userName)
        kubernetesDeleteServicesYaml(clusterName, 'jenkins',userName)
        kubernetesDeleteServicesYaml(clusterName, 'gitlab',userName)
        # 5. Delete Persist Volumes
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume.yml"],shell=True)
        subprocess.Popen([f"kubectl {action} -f ./kubernetes-deployments/storage/challenges/persistent-volume-claim.yml"],shell=True)
        # 6. Clean up the rest of environment (note this will close everything... do not do this in production)
        subprocess.Popen([f"kubectl delete po,svc,pv,pvc,deployment,configmap,replicaset,statefulset,ingress,secrets --all"],shell=True)

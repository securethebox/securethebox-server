import subprocess
import os
import requests
from lxml import html
import json
from subprocess import check_output
import urllib
import time
from ..infrastructure.docker import dockerGetContainerId
from ..infrastructure.kubernetes import kubernetesGetPodId
from ..services.gitlab import gitlabCreatePersonalAccessToken

"""
1. deploy,service,ingress - done
2. install plugin/extension via cli/script
3. connect to gitlab
3. connect to kubernetes host
4. trigger from gitlab push
5. deploy to kubernetes
"""

# Installs Gitlab & Git Plugin
# Go to http://jenkins-charles.us-west1-a.securethebox.us/updateCenter/ to see progress
def jenkinsInstallPlugin(clusterName,userName):
    url = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/pluginManager/install"
    
    payload = "json=%7B%20%22GitLab%22%3A%20%7B%22default%22%3A%20true%7D%2C%22docker-build-step%22%3A%7B%22default%22%3Atrue%7D%2C%22Kubernetes%20Continuous%20Deploy%22%3A%20%7B%22default%22%3A%20true%7D%2C%22Git%22%3A%20%7B%22default%22%3A%20true%7D%7D&dynamicLoad=Install%20without%20restart&plugin.git.default=on&plugin.gitlab-plugin.default=on&plugin.kubernetes-cd.default=on&plugin.docker-build-step.default=on"

    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Accept': "*/*",
        'Host': "jenkins-"+userName+"."+clusterName+".securethebox.us",
        'accept-encoding': "gzip, deflate",
        'content-length': "202",
        'Connection': "keep-alive"
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.status_code)
    print("Plugins should be installed")

def jenkinsRestartServer(clusterName,userName):
    url = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/restart"
    response = requests.request("GET", url)
    print(response.status_code)

    url2 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/restart"
    payload2 = "json=%7B%7D&Submit=Yes"
    response2 = requests.request("POST",url2,data=payload2)
    print(response2.status_code)

# 3.
def jenkinsConnectGitlab(api_token,clusterName,userName):
    # 1. Add Gitlab Credentials
    url1 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/descriptor/com.cloudbees.plugins.credentials.CredentialsSelectHelper/resolver/com.cloudbees.plugins.credentials.CredentialsSelectHelper$SystemContextResolver/provider/com.cloudbees.plugins.credentials.SystemCredentialsProvider$ProviderImpl/context/jenkins/addCredentials"
    headers1 = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # encoded_api_token = str(urllib.parse.quote(api_token))
    payload1 = "_.domain=_&_.scope=GLOBAL&_.username=&_.password=&_.id=&_.description=&stapler-class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl&%24class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl&_.scope=GLOBAL&_.apiToken="+api_token+"&_.id=gitlab-token&_.description=&stapler-class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl&%24class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl&stapler-class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey&%24class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey&stapler-class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl&%24class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl&json=%7B%22domain%22%3A+%22_%22%2C+%22%22%3A+%221%22%2C+%22credentials%22%3A+%7B%22scope%22%3A+%22GLOBAL%22%2C+%22apiToken%22%3A+%22"+api_token+"%22%2C+%22%24redact%22%3A+%22apiToken%22%2C+%22id%22%3A+%22gitlab-"+userName+"-root-token-id%22%2C+%22description%22%3A+%22%22%2C+%22stapler-class%22%3A+%22com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl%22%2C+%22%24class%22%3A+%22com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl%22%7D%7D"
    response1 = requests.request("POST",url1, data=payload1, headers=headers1)
    print("RESPONSE 2:",response1.status_code)

    #2. Test Connection
    url2 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/descriptorByName/com.dabsquared.gitlabjenkins.connection.GitLabConnectionConfig/testConnection"
    headers2 = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload2 = "apiTokenId=gitlab-"+userName+"-root-token-id&clientBuilderId=autodetect&url=http%3A%2F%2Fgitlab-"+userName+"&ignoreCertificateErrors=false"
    response2 = requests.request("POST",url2, data=payload2, headers=headers2)
    # Response should be Success
    print("RESPONSE 2:",response2.status_code)

    # 3. Apply
    url3 = "http://jenkins-"+userName+"."+clusterName+".securethebox.us/configSubmit"
    headers3 = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload3 = "system_message=&_.numExecutors=2&_.labelString=&master.mode=NORMAL&_.quietPeriod=5&_.scmCheckoutRetryCount=0&namingStrategy=0&stapler-class=jenkins.model.ProjectNamingStrategy%24DefaultProjectNamingStrategy&%24class=jenkins.model.ProjectNamingStrategy%24DefaultProjectNamingStrategy&stapler-class=jenkins.model.ProjectNamingStrategy%24PatternProjectNamingStrategy&%24class=jenkins.model.ProjectNamingStrategy%24PatternProjectNamingStrategy&_.namePattern=.*&_.description=&durabilityHint=null&_.usageStatisticsCollected=on&_.useAuthenticatedEndpoint=on&_.name=gitlab-"+userName+"-root-connection&id=com.dabsquared.gitlabjenkins.connection.GitLabConnection%40b025587&_.url=http%3A%2F%2Fgitlab-"+userName+"&_.apiTokenId=gitlab-"+userName+"-root-token-id&_.clientBuilderId=autodetect&_.connectionTimeout=10&_.readTimeout=10&_.appInsightsEnabled=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&administrativeMonitor=on&_.url=http%3A%2F%2Fjenkins-"+userName+"."+clusterName+".securethebox.us%2F&_.adminAddress=address+not+configured+yet+%3Cnobody%40nowhere%3E&_.globalConfigName=&_.globalConfigEmail=&_.shell=&_.dockerUrl=&_.dockerVersion=&_.dockerCertPath=&_.smtpServer=&_.defaultSuffix=&_.smtpAuthUserName=&_.smtpAuthPasswordSecret=&_.smtpPort=&_.replyToAddress=&_.charset=UTF-8&sendTestMailTo=&core%3Aapply=&json=%7B%22system_message%22%3A+%22%22%2C+%22jenkins-model-MasterBuildConfiguration%22%3A+%7B%22numExecutors%22%3A+%222%22%2C+%22labelString%22%3A+%22%22%2C+%22mode%22%3A+%22NORMAL%22%7D%2C+%22jenkins-model-GlobalQuietPeriodConfiguration%22%3A+%7B%22quietPeriod%22%3A+%225%22%7D%2C+%22jenkins-model-GlobalSCMRetryCountConfiguration%22%3A+%7B%22scmCheckoutRetryCount%22%3A+%220%22%7D%2C+%22jenkins-model-GlobalProjectNamingStrategyConfiguration%22%3A+%7B%7D%2C+%22jenkins-model-GlobalNodePropertiesConfiguration%22%3A+%7B%22globalNodeProperties%22%3A+%7B%7D%7D%2C+%22org-jenkinsci-plugins-workflow-flow-GlobalDefaultFlowDurabilityLevel%22%3A+%7B%22durabilityHint%22%3A+%22null%22%7D%2C+%22hudson-model-UsageStatistics%22%3A+%7B%22usageStatisticsCollected%22%3A+%7B%7D%7D%2C+%22com-dabsquared-gitlabjenkins-connection-GitLabConnectionConfig%22%3A+%7B%22useAuthenticatedEndpoint%22%3A+true%2C+%22connections%22%3A+%7B%22name%22%3A+%22gitlab-"+userName+"-root-connection%22%2C+%22id%22%3A+%22com.dabsquared.gitlabjenkins.connection.GitLabConnection%40b025587%22%2C+%22url%22%3A+%22http%3A%2F%2Fgitlab-"+userName+"%22%2C+%22apiTokenId%22%3A+%22gitlab-"+userName+"-root-token-id%22%2C+%22clientBuilderId%22%3A+%22autodetect%22%2C+%22ignoreCertificateErrors%22%3A+false%2C+%22connectionTimeout%22%3A+%2210%22%2C+%22readTimeout%22%3A+%2210%22%7D%7D%2C+%22app-insights-plugin-configuration%22%3A+%7B%22appInsightsEnabled%22%3A+true%7D%2C+%22jenkins-management-AdministrativeMonitorsConfiguration%22%3A+%7B%22administrativeMonitor%22%3A+%5B%22hudson.PluginManager%24PluginCycleDependenciesMonitor%22%2C+%22hudson.PluginManager%24PluginUpdateMonitor%22%2C+%22hudson.PluginWrapper%24PluginWrapperAdministrativeMonitor%22%2C+%22hudsonHomeIsFull%22%2C+%22hudson.diagnosis.NullIdDescriptorMonitor%22%2C+%22OldData%22%2C+%22hudson.diagnosis.ReverseProxySetupMonitor%22%2C+%22hudson.diagnosis.TooManyJobsButNoView%22%2C+%22hudson.model.UpdateCenter%24CoreUpdateMonitor%22%2C+%22hudson.node_monitors.MonitorMarkedNodeOffline%22%2C+%22hudson.triggers.SCMTrigger%24AdministrativeMonitorImpl%22%2C+%22jenkins.diagnosis.HsErrPidList%22%2C+%22jenkins.diagnostics.CompletedInitializationMonitor%22%2C+%22jenkins.diagnostics.RootUrlNotSetMonitor%22%2C+%22jenkins.diagnostics.SecurityIsOffMonitor%22%2C+%22jenkins.diagnostics.URICheckEncodingMonitor%22%2C+%22jenkins.model.DownloadSettings%24Warning%22%2C+%22jenkins.model.Jenkins%24EnforceSlaveAgentPortAdministrativeMonitor%22%2C+%22jenkins.security.QueueItemAuthenticatorMonitor%22%2C+%22jenkins.security.RekeySecretAdminMonitor%22%2C+%22jenkins.security.UpdateSiteWarningsMonitor%22%2C+%22jenkins.security.apitoken.ApiTokenPropertyDisabledDefaultAdministrativeMonitor%22%2C+%22jenkins.security.apitoken.ApiTokenPropertyEnabledNewLegacyAdministrativeMonitor%22%2C+%22legacyApiToken%22%2C+%22jenkins.security.csrf.CSRFAdministrativeMonitor%22%2C+%22slaveToMasterAccessControl%22%2C+%22jenkins.security.s2m.MasterKillSwitchWarning%22%2C+%22jenkins.slaves.DeprecatedAgentProtocolMonitor%22%5D%7D%2C+%22jenkins-model-JenkinsLocationConfiguration%22%3A+%7B%22url%22%3A+%22http%3A%2F%2Fjenkins-"+userName+"."+clusterName+".securethebox.us%2F%22%2C+%22adminAddress%22%3A+%22address+not+configured+yet+%3Cnobody%40nowhere%3E%22%7D%2C+%22hudson-plugins-git-GitSCM%22%3A+%7B%22globalConfigName%22%3A+%22%22%2C+%22globalConfigEmail%22%3A+%22%22%2C+%22createAccountBasedOnEmail%22%3A+false%7D%2C+%22hudson-tasks-Shell%22%3A+%7B%22shell%22%3A+%22%22%7D%2C+%22org-jenkinsci-plugins-dockerbuildstep-DockerBuilder%22%3A+%7B%22dockerUrl%22%3A+%22%22%2C+%22dockerVersion%22%3A+%22%22%2C+%22dockerCertPath%22%3A+%22%22%7D%2C+%22hudson-tasks-Mailer%22%3A+%7B%22smtpServer%22%3A+%22%22%2C+%22defaultSuffix%22%3A+%22%22%2C+%22useSsl%22%3A+false%2C+%22smtpPort%22%3A+%22%22%2C+%22replyToAddress%22%3A+%22%22%2C+%22charset%22%3A+%22UTF-8%22%7D%2C+%22core%3Aapply%22%3A+%22%22%7D&Submit=Save"
    # Response should be saved
    response3 = requests.request("POST",url3, data=payload3, headers=headers3)
    print("RESPONSE 3:",response3.status_code)
    print("Jenkins should be connected to gitlab")

    # generate ssh keypair with no password (within container)
def jenkinsCreateSSHKeypair(serviceName,userName):
    pod_id = kubernetesGetPodId(serviceName,userName)
    container_id = dockerGetContainerId(pod_id)
    subprocess.Popen([f"docker exec -i "+container_id+"  bash -c \"ssh-keygen -f id_rsa -t rsa -N ''\""],shell=True).wait()

def jenkinsGetSSHPublicKey(serviceName,userName):
    pod_id = kubernetesGetPodId(serviceName,userName)
    container_id = dockerGetContainerId(pod_id)
    public = check_output(["docker", "exec","-i",container_id,"bash","-c","cat id_rsa.pub"])
    ssh_public_key = public.decode("utf-8")
    print("PUBLIC KEY:",ssh_public_key)
    return ssh_public_key

def jenkinsGetSSHPrivateKey(serviceName,userName):
    pod_id = kubernetesGetPodId(serviceName,userName)
    print("POD ID:",pod_id)
    container_id = dockerGetContainerId(pod_id)
    print("CONTAINER ID:",container_id)
    private = check_output(["docker", "exec","-i",container_id,"bash","-c","cat id_rsa"])
    ssh_private_key = private.decode("utf-8")
    # print("PRIVATE KEY:",ssh_private_key)
    return ssh_private_key

def jenkinsJobAddSourceCodeManagement():
    # source code management in jenkins:
    # http://gitlab-charles/root/juice-shop-charles
    print()

def jenkinsCredentialsAddSSHPrivateKey(private_key):
    # url1 = "http://jenkins-charles.us-west1-a.securethebox.us/descriptor/com.cloudbees.plugins.credentials.CredentialsSelectHelper/resolver/com.cloudbees.plugins.credentials.CredentialsSelectHelper$SystemContextResolver/provider/com.cloudbees.plugins.credentials.SystemCredentialsProvider$ProviderImpl/context/jenkins/addCredentials"
    url1 = "http://jenkins-charles.us-west1-a.securethebox.us/credentials/store/system/domain/_/createCredentials"
    headers1 = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    # print(private_key)
    # private_key_encoded = urllib.parse.quote_plus(private_key)
    # print(private_key_encoded)
    print(private_key)
    private_key_encoded = urllib.parse.quote_plus(private_key.rstrip())
    private_key_encoded_nl = urllib.parse.quote_plus(str(private_key.rstrip().replace("\n","\\n")))
    print(private_key_encoded)
    print(private_key_encoded_nl)

    payload1 =  "_.scope=GLOBAL&_.username=&_.password=&_.id=&_.description=&stapler-class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl&%24class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl&stapler-class=org.jenkinsci.plugins.docker.commons.credentials.DockerServerCredentials&%24class=org.jenkinsci.plugins.docker.commons.credentials.DockerServerCredentials&stapler-class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl&%24class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl&stapler-class=com.microsoft.jenkins.kubernetes.credentials.KubeconfigCredentials&%24class=com.microsoft.jenkins.kubernetes.credentials.KubeconfigCredentials&_.scope=GLOBAL&_.id=jenkins-charles-root-private-key&_.description=&_.username=jenkins&id270.privateKeySource=0\\&\\_.privateKey=\
        "+private_key_encoded+"\
            &stapler-class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey%24DirectEntryPrivateKeySource&%24class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey%24DirectEntryPrivateKeySource&_.passphrase=&stapler-class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey&%24class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey&stapler-class=org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl&%24class=org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl&stapler-class=org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl&%24class=org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl&stapler-class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl&%24class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl&json=%7B%22%22%3A+%224%22%2C+%22credentials%22%3A+%7B%22scope%22%3A+%22GLOBAL%22%2C+%22id%22%3A+%22jenkins-charles-root-private-key%22%2C+%22description%22%3A+%22%22%2C+%22username%22%3A+%22jenkins%22%2C+%22privateKeySource%22%3A+%7B%22value%22%3A+%220%22%2C+%22privateKey%22%3A+%22\
                "+private_key_encoded_nl+"\
                    %22%2C+%22stapler-class%22%3A+%22com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey%24DirectEntryPrivateKeySource%22%2C+%22%24class%22%3A+%22com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey%24DirectEntryPrivateKeySource%22%7D%2C+%22passphrase%22%3A+%22%22%2C+%22%24redact%22%3A+%22passphrase%22%2C+%22stapler-class%22%3A+%22com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey%22%2C+%22%24class%22%3A+%22com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey%22%7D%7D&Submit=OK"
    response1 = requests.request("POST",url1, data=payload1, headers=headers1)
    print(response1.status_code)

def jenkinsCredentialsAddSCM():
    print()

def jenkinsCreateJob(serviceName,userName):
    # Need to install plugins first
    # job title: deploy-to-kubernetes
    url1 = "http://jenkins-"+userName+".us-west1-a.securethebox.us/view/all/createItem"
    headers1 = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload1 = "name=deploy-to-kubernetes&mode=hudson.model.FreeStyleProject&json=%7B%22name%22%3A+%22deploy-to-kubernetes%22%2C+%22mode%22%3A+%22hudson.model.FreeStyleProject%22%7D"
    response1 = requests.request("POST",url1, data=payload1, headers=headers1)
    print(response1.status_code)

    # add private key to job
    private_key = jenkinsGetSSHPrivateKey(serviceName,userName)
    jenkinsCredentialsAddSSHPrivateKey(private_key)
    # add shell command to juice-shop app
    pod_id = kubernetesGetPodId('juice-shop',userName)
    container_id = dockerGetContainerId(pod_id)
    # save job
    url2 = "http://jenkins-"+userName+".us-west1-a.securethebox.us/job/deploy-to-kubernetes/configSubmit"
    headers2 = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload2 = "description=&stapler-class-bag=true&_.daysToKeepStr=&_.numToKeepStr=&_.artifactDaysToKeepStr=&_.artifactNumToKeepStr=&stapler-class=hudson.tasks.LogRotator&%24class=hudson.tasks.LogRotator&_.gitLabConnection=gitlab-charles-root-connection&quiet_period=5&scmCheckoutRetryCount=0&_.customWorkspace=&_.displayNameOrNull=&stapler-class=hudson.scm.NullSCM&%24class=hudson.scm.NullSCM&scm=1&stapler-class=hudson.plugins.git.GitSCM&%24class=hudson.plugins.git.GitSCM&_.url=http%3A%2F%2Fgitlab-charles%2Froot%2Fjuice-shop-charles&_.credentialsId=jenkins-charles-root-private-key&_.name=&_.refspec=&_.name=*%2Fmaster&stapler-class=hudson.plugins.git.browser.AssemblaWeb&%24class=hudson.plugins.git.browser.AssemblaWeb&stapler-class=hudson.plugins.git.browser.FisheyeGitRepositoryBrowser&%24class=hudson.plugins.git.browser.FisheyeGitRepositoryBrowser&stapler-class=hudson.plugins.git.browser.KilnGit&%24class=hudson.plugins.git.browser.KilnGit&stapler-class=hudson.plugins.git.browser.TFS2013GitRepositoryBrowser&%24class=hudson.plugins.git.browser.TFS2013GitRepositoryBrowser&stapler-class=hudson.plugins.git.browser.BitbucketWeb&%24class=hudson.plugins.git.browser.BitbucketWeb&stapler-class=hudson.plugins.git.browser.CGit&%24class=hudson.plugins.git.browser.CGit&stapler-class=hudson.plugins.git.browser.GitBlitRepositoryBrowser&%24class=hudson.plugins.git.browser.GitBlitRepositoryBrowser&stapler-class=hudson.plugins.git.browser.GithubWeb&%24class=hudson.plugins.git.browser.GithubWeb&stapler-class=hudson.plugins.git.browser.Gitiles&%24class=hudson.plugins.git.browser.Gitiles&stapler-class=hudson.plugins.git.browser.GitLab&%24class=hudson.plugins.git.browser.GitLab&stapler-class=hudson.plugins.git.browser.GitList&%24class=hudson.plugins.git.browser.GitList&stapler-class=hudson.plugins.git.browser.GitoriousWeb&%24class=hudson.plugins.git.browser.GitoriousWeb&stapler-class=hudson.plugins.git.browser.GitWeb&%24class=hudson.plugins.git.browser.GitWeb&stapler-class=hudson.plugins.git.browser.GogsGit&%24class=hudson.plugins.git.browser.GogsGit&stapler-class=hudson.plugins.git.browser.Phabricator&%24class=hudson.plugins.git.browser.Phabricator&stapler-class=hudson.plugins.git.browser.RedmineWeb&%24class=hudson.plugins.git.browser.RedmineWeb&stapler-class=hudson.plugins.git.browser.RhodeCode&%24class=hudson.plugins.git.browser.RhodeCode&stapler-class=hudson.plugins.git.browser.Stash&%24class=hudson.plugins.git.browser.Stash&stapler-class=hudson.plugins.git.browser.ViewGitWeb&%24class=hudson.plugins.git.browser.ViewGitWeb&_.upstreamProjects=&ReverseBuildTrigger.threshold=SUCCESS&_.spec=&com-dabsquared-gitlabjenkins-GitLabPushTrigger=on&_.triggerOnPush=on&_.triggerOpenMergeRequestOnPush=never&_.noteRegex=Jenkins+please+retry+a+build&_.ciSkip=on&_.skipWorkInProgressMergeRequest=on&_.setBuildDescription=on&_.pendingBuildName=&branchFilterType=All&includeBranchesSpec=&excludeBranchesSpec=&sourceBranchRegex=&targetBranchRegex=&include=&exclude=&_.secretToken=&_.scmpoll_spec=&command=docker+exec+-i+"+container_id+"+bash+-c+%22cd+juice-shop-charles+%3B+git+pull%22&_.unstableReturn=&stapler-class=hudson.tasks.Shell&%24class=hudson.tasks.Shell&core%3Aapply=&json=%7B%22description%22%3A+%22%22%2C+%22properties%22%3A+%7B%22stapler-class-bag%22%3A+%22true%22%2C+%22jenkins-model-BuildDiscarderProperty%22%3A+%7B%22specified%22%3A+false%2C+%22%22%3A+%220%22%2C+%22strategy%22%3A+%7B%22daysToKeepStr%22%3A+%22%22%2C+%22numToKeepStr%22%3A+%22%22%2C+%22artifactDaysToKeepStr%22%3A+%22%22%2C+%22artifactNumToKeepStr%22%3A+%22%22%2C+%22stapler-class%22%3A+%22hudson.tasks.LogRotator%22%2C+%22%24class%22%3A+%22hudson.tasks.LogRotator%22%7D%7D%2C+%22com-dabsquared-gitlabjenkins-connection-GitLabConnectionProperty%22%3A+%7B%22gitLabConnection%22%3A+%22gitlab-charles-root-connection%22%7D%2C+%22hudson-model-ParametersDefinitionProperty%22%3A+%7B%22specified%22%3A+false%7D%7D%2C+%22disable%22%3A+false%2C+%22concurrentBuild%22%3A+false%2C+%22hasCustomQuietPeriod%22%3A+false%2C+%22quiet_period%22%3A+%225%22%2C+%22hasCustomScmCheckoutRetryCount%22%3A+false%2C+%22scmCheckoutRetryCount%22%3A+%220%22%2C+%22blockBuildWhenUpstreamBuilding%22%3A+false%2C+%22blockBuildWhenDownstreamBuilding%22%3A+false%2C+%22hasCustomWorkspace%22%3A+false%2C+%22customWorkspace%22%3A+%22%22%2C+%22displayNameOrNull%22%3A+%22%22%2C+%22scm%22%3A+%7B%22value%22%3A+%221%22%2C+%22stapler-class%22%3A+%22hudson.plugins.git.GitSCM%22%2C+%22%24class%22%3A+%22hudson.plugins.git.GitSCM%22%2C+%22userRemoteConfigs%22%3A+%7B%22url%22%3A+%22http%3A%2F%2Fgitlab-charles%2Froot%2Fjuice-shop-charles%22%2C+%22credentialsId%22%3A+%22jenkins-charles-root-private-key%22%2C+%22name%22%3A+%22%22%2C+%22refspec%22%3A+%22%22%7D%2C+%22branches%22%3A+%7B%22name%22%3A+%22*%2Fmaster%22%7D%2C+%22%22%3A+%22auto%22%7D%2C+%22com-dabsquared-gitlabjenkins-GitLabPushTrigger%22%3A+%7B%22triggerOnPush%22%3A+true%2C+%22triggerOnMergeRequest%22%3A+false%2C+%22triggerOnAcceptedMergeRequest%22%3A+false%2C+%22triggerOnClosedMergeRequest%22%3A+false%2C+%22triggerOpenMergeRequestOnPush%22%3A+%22never%22%2C+%22triggerOnApprovedMergeRequest%22%3A+false%2C+%22triggerOnNoteRequest%22%3A+false%2C+%22noteRegex%22%3A+%22Jenkins+please+retry+a+build%22%2C+%22ciSkip%22%3A+true%2C+%22skipWorkInProgressMergeRequest%22%3A+true%2C+%22setBuildDescription%22%3A+true%2C+%22triggerOnPipelineEvent%22%3A+false%2C+%22pendingBuildName%22%3A+%22%22%2C+%22cancelPendingBuildsOnUpdate%22%3A+false%2C+%22branchFilterType%22%3A+%22All%22%2C+%22includeBranchesSpec%22%3A+%22%22%2C+%22excludeBranchesSpec%22%3A+%22%22%2C+%22sourceBranchRegex%22%3A+%22%22%2C+%22targetBranchRegex%22%3A+%22%22%2C+%22secretToken%22%3A+%22%22%7D%2C+%22builder%22%3A+%7B%22command%22%3A+%22docker+exec+-i+"+container_id+"+bash+-c+%5C%22cd+juice-shop-charles+%3B+git+pull%5C%22%22%2C+%22%22%3A+%22docker+exec+-i+"+container_id+"+bash+-c+%5C%22cd+juice-shop-charles+%3B+git+pull%5C%22%22%2C+%22unstableReturn%22%3A+%22%22%2C+%22stapler-class%22%3A+%22hudson.tasks.Shell%22%2C+%22%24class%22%3A+%22hudson.tasks.Shell%22%7D%2C+%22core%3Aapply%22%3A+%22%22%7D&Submit=Save"

    response2 = requests.request("POST",url2, data=payload2, headers=headers2)
    print(response2.status_code)

    
    # source code management in jenkins (must make repo public and add public key first):
    # Repository URL: http://gitlab-"+userName+"/root/juice-shop-"+userName

    # Run docker command in container to update changes
    # docker exec -i 557ccefcc2ca  bash -c "cd juice-shop-charles ; git pull"

def main():
    # jenkinsInstallPlugin("us-west1-a","charles")
    # time.sleep(30)
    # api_token = gitlabCreatePersonalAccessToken()
    # print("API TOKEN:",api_token)
    # jenkinsConnectGitlab(api_token,"us-west1-a","charles")
    # time.sleep(30)
    # jenkinsRestartServer("us-west1-a","charles")
    # print("DONE")
    # time.sleep(30)
    # jenkinsCreateSSHKeypair('jenkins','charles')
    # jenkinsGetSSHPrivateKey('jenkins','charles')
    # before creating job, app needs to be deployed
    # jenkinsCreateJob('jenkins','charles')
    private_key = jenkinsGetSSHPrivateKey('jenkins','charles')
    # print(private_key)
    jenkinsCredentialsAddSSHPrivateKey(private_key)
    print("This is done")

if __name__ == "__main__":
    main()
import subprocess
import os
import requests
from lxml import html
import urllib
import gitlab
import datetime

"""
1. deploy,service,ingress ( ~100 seconds ) - done
2. reset root password on gitlab - done
3. clone,commit,push juice-shop to gitlab - done
4. generate API Token - done
5. make repository public - done
6. enable outbound requests - done
7. add deploy key (ssh public key from jenkins) - done
8. add webhook url and disable ssl verification - done
"""

def gitlabCreateProject(clusterName, userName):
    """
    1. cd into apps directory
    2. git clone juice-shop-+username
    3. delete existing git
    4. commit,push to gitlab
    """
    os.chdir('../repositories')
    print("CWD:",os.getcwd())
    print("DELETING EXISTING PROJECT")
    subprocess.Popen([f"rm -rf juice-shop-"+userName],shell=True).wait()
    # make sure this server has 'git' installed
    subprocess.Popen([f"git clone https://github.com/ncmd/juice-shop.git juice-shop-"+userName],shell=True).wait()
    os.chdir('./juice-shop-'+userName)
    print("CWD:",os.getcwd())
    subprocess.Popen([f"rm -rf .git"],shell=True).wait()
    subprocess.Popen([f"git init"],shell=True).wait()
    subprocess.Popen([f"git add ."],shell=True).wait()
    subprocess.Popen([f"git commit -m 'production app'"],shell=True).wait()
    subprocess.Popen([f"git push --set-upstream http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-"+userName+".git master"],shell=True).wait()


def gitlabGetResetPasswordToken(clusterName,userName):
    url = "http://gitlab-"+userName+"."+clusterName+".securethebox.us"
    headers = {
        'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us"
        }
    response = requests.request("GET", url, headers=headers, allow_redirects=True)
    response_url = response.url
    password_token = response_url.split('=')
    # print("PASSWORD TOKEN:",password_token[1])
    session_cookie = response.request.headers['Cookie']
    # print("SESSION COOKIE:",response.request.headers['Cookie'])
    return password_token[1],session_cookie
    
def gitlabPostResetPassword(token,session,clusterName,userName):
    url = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/password/edit?reset_password_token="+token
    headers = {
        'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie':session
        }
    page = requests.request("GET", url, headers=headers)
    tree = html.fromstring(page.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    # print("HEADERS:",headers)
    form_data = {
        "utf8": "✓",
        "_method": "put",
        "authenticity_token": authtoken[0].value,
        "user[reset_password_token]": token,
        "user[password]": "Changeme",
        "user[password_confirmation]": "Changeme",
    }
    submit_url = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/password"
    # print("FORM DATA:",form_data)
    submitform = requests.request("POST", submit_url, headers=headers, data=form_data)
    print("gitlabPostResetPassword STATUS CODE:",submitform.status_code)

    # 1. GET request to get csrf authenticity-token on sign_in page
    # 2. Submit login form follow redirect
    # 3. Get Cookie/Session header
    # 4. GET request to personal_access_tokens page
    # 5. Submit token form
    # 6. Follow redirect to generated personal access token

def gitlabCreatePersonalAccessToken():
    # 1
    url1 = "http://gitlab-charles.us-west1-a.securethebox.us/users/sign_in"
    response1 = requests.request("GET", url1)
    session_cookie1 = response1.headers['Set-Cookie'].split(';')
    # print("Guest Session Cookie:",session_cookie1[0])
    tree = html.fromstring(response1.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    # print("Guest authenticity_token:",authtoken[0].value)
    new_auth_token = urllib.parse.quote(authtoken[0].value)
    # print("Guest Encoded authenticity_token:",new_auth_token)

    # 2
    url2 = "http://gitlab-charles.us-west1-a.securethebox.us/users/sign_in"
    payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token+"&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "gitlab-charles.us-west1-a.securethebox.us",
        'Cookie': session_cookie1[0]
        }
    response2 = requests.request("POST", url2, data=payload, headers=headers, allow_redirects=True)
    session_cookie2 = response2.request.headers['Cookie']
    # print("User Session Cookie2:",session_cookie2)
    tree2 = html.fromstring(response2.content)
    authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
    print("User authenticity_token2:",authtoken2)
    # 3
    url3 = "http://gitlab-charles.us-west1-a.securethebox.us/profile/personal_access_tokens"
    headers3 = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Host': "gitlab-charles.us-west1-a.securethebox.us",
    'Cookie': session_cookie2
    }
    response3 = requests.request("GET", url3, headers=headers3)
    session_cookie3 = response3.request.headers['Cookie']
    # print("User Session Cookie3:",session_cookie3)
    tree3 = html.fromstring(response3.content)
    authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
    # print("User csrf-token for personal_access_token page:",authtoken3[0].attrib['content'])
    
    # 4
    now = datetime.datetime.now()
    year100 = now.year + 100
    print(year100)
    url4 = "http://gitlab-charles.us-west1-a.securethebox.us/profile/personal_access_tokens"
    payload = "utf8=%E2%9C%93&authenticity_token="+urllib.parse.quote(authtoken3[0].attrib['content'])+"&personal_access_token%5Bname%5D=jenkins-charles-root&personal_access_token%5Bexpires_at%5D="+str(year100)+"-"+str(now.day)+"-"+str(now.month)+"&personal_access_token%5Bscopes%5D%5B%5D=api&personal_access_token%5Bscopes%5D%5B%5D=read_user&personal_access_token%5Bscopes%5D%5B%5D=read_repository&personal_access_token%5Bscopes%5D%5B%5D=write_repository&personal_access_token%5Bscopes%5D%5B%5D=sudo"
    headers4 = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "gitlab-charles.us-west1-a.securethebox.us",
        'Cookie': session_cookie3,
        'accept-encoding': "gzip, deflate",
        'Connection': "keep-alive"
        }

    response4 = requests.request("POST", url4, data=payload, headers=headers4, allow_redirects=True)
    print(response4.status_code)

    # 5
    url5 = "http://gitlab-charles.us-west1-a.securethebox.us/profile/personal_access_tokens"
    headers5 = {
        'Host': "gitlab-charles.us-west1-a.securethebox.us",
        'Cookie': session_cookie3
        }
    response5 = requests.request("GET", url5, headers=headers5)
    tree5 = html.fromstring(response5.content)
    authtoken5 = tree5.xpath('//input[@name="created-personal-access-token"]')
    return authtoken5[0].value

    # 1. make repository public
    # Settings > General > Visibility 
def gitlabMakeProjectPublic(clusterName,userName):
    url1 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    response1 = requests.request("GET", url1)
    session_cookie1 = response1.headers['Set-Cookie'].split(';')
    # print("Guest Session Cookie:",session_cookie1[0])
    tree = html.fromstring(response1.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    # print("Guest authenticity_token:",authtoken[0].value)
    new_auth_token = urllib.parse.quote(authtoken[0].value)
    # print("Guest Encoded authenticity_token:",new_auth_token)

    # 2
    url2 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token+"&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "gitlab-charles.us-west1-a.securethebox.us",
        'Cookie': session_cookie1[0]
        }
    response2 = requests.request("POST", url2, data=payload, headers=headers, allow_redirects=True)
    session_cookie2 = response2.request.headers['Cookie']
    # print("User Session Cookie2:",session_cookie2)
    tree2 = html.fromstring(response2.content)
    authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
    print("User authenticity_token2:",authtoken2)

    # 3
    url3 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-"+userName+"/edit"
    headers3 = {
    'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
    'Cookie': session_cookie2
    }
    response3 = requests.request("GET", url3, headers=headers3)
    session_cookie3 = response3.request.headers['Cookie']
    # print("User Session Cookie3:",session_cookie3)
    tree3 = html.fromstring(response3.content)
    authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
    print("User csrf-token for personal_access_token page:",authtoken3[0].attrib['content'])

    url4 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-"+userName
    # "Cookie": _gitlab_session=a7d17d16b5a99b5207e10782fd03a9bb
    # X-CSRF-Token: DjGSD8p5IGNTrEtOhDHcK6AkUfr28iyw+dpX95Czs1mHVAZdiNzxDiuC+gO2s+fSfe8GvkBzii3RYT4rROcwfg==
    headers4 = {
        "Cookie": session_cookie3,
        "X-CSRF-Token":authtoken3[0].attrib['content']
    }
    
    auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
    payload4 = "utf8=%E2%9C%93&_method=patch&authenticity_token="+auth_token4+"&update_section=js-shared-permissions&project%5Bvisibility_level%5D=20&project%5Brequest_access_enabled%5D=true&project%5Bproject_feature_attributes%5D%5Bissues_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Brepository_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Bmerge_requests_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Bbuilds_access_level%5D=20&project%5Blfs_enabled%5D=true&project%5Bproject_feature_attributes%5D%5Bwiki_access_level%5D=20&project%5Bproject_feature_attributes%5D%5Bsnippets_access_level%5D=20&commit=Save+changes"

    response4 = requests.request("POST", url4, headers=headers4, data=payload4)
    print("Response code:",response4.status_code)

    # 2. enable outbound requests
    # http://gitlab-charles.us-west1-a.securethebox.us/admin/application_settings/network
    # Allow requests to the local network from hooks and services
def gitlabProjectAllowOutbound(clusterName,userName):
    url1 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    response1 = requests.request("GET", url1)
    session_cookie1 = response1.headers['Set-Cookie'].split(';')
    # print("Guest Session Cookie:",session_cookie1[0])
    tree = html.fromstring(response1.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    # print("Guest authenticity_token:",authtoken[0].value)
    new_auth_token = urllib.parse.quote(authtoken[0].value)
    # print("Guest Encoded authenticity_token:",new_auth_token)

    # 2
    url2 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token+"&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
        'Cookie': session_cookie1[0]
        }
    response2 = requests.request("POST", url2, data=payload, headers=headers, allow_redirects=True)
    session_cookie2 = response2.request.headers['Cookie']
    # print("User Session Cookie2:",session_cookie2)
    tree2 = html.fromstring(response2.content)
    authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
    print("User authenticity_token2:",authtoken2)

    # 3
    url3 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/admin/application_settings/network"
    headers3 = {
    'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
    'Cookie': session_cookie2
    }
    response3 = requests.request("GET", url3, headers=headers3)
    session_cookie3 = response3.request.headers['Cookie']
    # print("User Session Cookie3:",session_cookie3)
    tree3 = html.fromstring(response3.content)
    authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
    print("User csrf-token for personal_access_token page:",authtoken3[0].attrib['content'])

    url4 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/admin/application_settings"
    headers4 = {
        "Cookie": session_cookie3,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
    payload4 = "utf8=%E2%9C%93&_method=patch&authenticity_token="+auth_token4+"&application_setting%5Ballow_local_requests_from_hooks_and_services%5D=0&application_setting%5Ballow_local_requests_from_hooks_and_services%5D=1&application_setting%5Bdns_rebinding_protection_enabled%5D=0&application_setting%5Bdns_rebinding_protection_enabled%5D=0"

    response4 = requests.request("POST", url4, headers=headers4, data=payload4)
    print("Response code:",response4.status_code)

    # Install Jenkins public key as a deploy key for project juice-shop-charles
    # title: jenkins-charles-root-public-key
    # enable write access
    # settings > Repository > Deploy keys

def gitlabProjectAddDeployKey(jenkins_public_key,clusterName,userName):
    url1 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    response1 = requests.request("GET", url1)
    session_cookie1 = response1.headers['Set-Cookie'].split(';')
    # print("Guest Session Cookie:",session_cookie1[0])
    tree = html.fromstring(response1.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    # print("Guest authenticity_token:",authtoken[0].value)
    new_auth_token = urllib.parse.quote(authtoken[0].value)
    # print("Guest Encoded authenticity_token:",new_auth_token)

    # 2
    url2 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token+"&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
        'Cookie': session_cookie1[0]
        }
    response2 = requests.request("POST", url2, data=payload, headers=headers, allow_redirects=True)
    session_cookie2 = response2.request.headers['Cookie']
    # print("User Session Cookie2:",session_cookie2)
    tree2 = html.fromstring(response2.content)
    authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
    print("User authenticity_token2:",authtoken2)

    # 3
    url3 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-charles/settings/repository"
    headers3 = {
    'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
    'Cookie': session_cookie2
    }
    response3 = requests.request("GET", url3, headers=headers3)
    session_cookie3 = response3.request.headers['Cookie']
    # print("User Session Cookie3:",session_cookie3)
    tree3 = html.fromstring(response3.content)
    authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
    print("User csrf-token for personal_access_token page:",authtoken3[0].attrib['content'])

    url4 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-"+userName+"/deploy_keys"
    headers4 = {
        "Cookie": session_cookie3,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
    # jenkins_public_key = jenkinsGetSSHPublicKey('jenkins','charles')
    jenkins_public_key_urlencoded = urllib.parse.quote(jenkins_public_key)
    payload4 = "utf8=%E2%9C%93&authenticity_token="+auth_token4+"&deploy_key%5Btitle%5D=jenkins-charles-root-public-key\
        &deploy_key%5Bkey%5D="+jenkins_public_key_urlencoded+"\
        &deploy_key%5Bdeploy_keys_projects_attributes%5D%5B0%5D%5Bcan_push%5D=0\
        &deploy_key%5Bdeploy_keys_projects_attributes%5D%5B0%5D%5Bcan_push%5D=1"

    response4 = requests.request("POST", url4, headers=headers4, data=payload4)
    print("Response code:",response4.status_code)

    # integrations
    # Add webhook url and disable ssl verification
    # http://jenkins-charles/project/deploy-to-kubernetes
def gitlabProjectAddWebhook(clusterName,userName):
    url1 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    response1 = requests.request("GET", url1)
    session_cookie1 = response1.headers['Set-Cookie'].split(';')
    # print("Guest Session Cookie:",session_cookie1[0])
    tree = html.fromstring(response1.content)
    authtoken = tree.xpath('//input[@name="authenticity_token"]')
    # print("Guest authenticity_token:",authtoken[0].value)
    new_auth_token = urllib.parse.quote(authtoken[0].value)
    # print("Guest Encoded authenticity_token:",new_auth_token)
    # print(response1.status_code)

    # 2
    url2 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/users/sign_in"
    payload = "utf8=%E2%9C%93&authenticity_token="+new_auth_token+"&user%5Blogin%5D=root&user%5Bpassword%5D=Changeme&user%5Bremember_me%5D=0"
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
        'Cookie': session_cookie1[0]
        }
    response2 = requests.request("POST", url2, data=payload, headers=headers, allow_redirects=True)
    session_cookie2 = response2.request.headers['Cookie']
    # print("User Session Cookie2:",session_cookie2)
    tree2 = html.fromstring(response2.content)
    authtoken2 = tree2.xpath('//input[@name="authenticity_token"]')
    print("User authenticity_token2:",authtoken2)
    # print(response2.status_code)

    # 3
    url3 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-"+userName+"/settings/integrations"
    headers3 = {
    'Host': "gitlab-"+userName+"."+clusterName+".securethebox.us",
    'Cookie': session_cookie2
    }
    response3 = requests.request("GET", url3, headers=headers3)
    session_cookie3 = response3.request.headers['Cookie']
    # print("User Session Cookie3:",session_cookie3)
    tree3 = html.fromstring(response3.content)
    authtoken3 = tree3.xpath('//meta[@name="csrf-token"]')
    # print("User csrf-token for personal_access_token page:",authtoken3[0].attrib['content'])
    # print(response3.status_code)

    # this url changes!!!
    url4 = "http://gitlab-"+userName+"."+clusterName+".securethebox.us/root/juice-shop-"+userName+"/hooks"
    headers4 = {
        "Cookie": session_cookie3,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    auth_token4 = urllib.parse.quote(authtoken3[0].attrib['content'])
    # print("auth_token4",auth_token4)
    payload4 = "utf8=%E2%9C%93&authenticity_token="+auth_token4+"&hook%5Burl%5D=http%3A%2F%2Fjenkins-charles%3A8080%2Fproject%2Fdeploy-to-kubernetes&hook%5Btoken%5D=&hook%5Bpush_events%5D=0&hook%5Bpush_events%5D=1&hook%5Bpush_events_branch_filter%5D=&hook%5Btag_push_events%5D=0&hook%5Bnote_events%5D=0&hook%5Bconfidential_note_events%5D=0&hook%5Bissues_events%5D=0&hook%5Bconfidential_issues_events%5D=0&hook%5Bmerge_requests_events%5D=0&hook%5Bjob_events%5D=0&hook%5Bpipeline_events%5D=0&hook%5Bwiki_page_events%5D=0&hook%5Benable_ssl_verification%5D=0"
    response4 = requests.request("POST", url4, headers=headers4, data=payload4, allow_redirects=True)
    print("Response code:",response4.status_code)

def main():
    try:
        reset_token,session_cookie = gitlabGetResetPasswordToken('us-west1-a','charles')
        gitlabPostResetPassword(reset_token,session_cookie,'us-west1-a','charles')
        gitlabCreateProject('us-west1-a', 'charles')
        gitlabMakeProjectPublic('us-west1-a', 'charles')
        gitlabProjectAllowOutbound('us-west1-a', 'charles')
        gitlabProjectAddWebhook('us-west1-a', 'charles')

        # Install deploy key
        # public_key = jenkinsGetSSHPublicKey('jenkins','charles')
        # gitlabProjectAddDeployKey(public_key)
        # After finishing this, need to deploy app

    except:
        print("Already did it")
   

if __name__ == "__main__":
    main()
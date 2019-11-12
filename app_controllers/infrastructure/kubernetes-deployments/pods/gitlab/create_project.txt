import subprocess
import os

def createGitlabProject(serviceName, userName):
    pod_id = getPodId(serviceName, userName)

    # make sure this server has 'git' installed
    subprocess.Popen([f"git clone https://github.com/ncmd/juice-shop.git juice-shop-"+userName],shell=True).wait()
    os.chdir('./juice-shop-'+userName)
    print("CWD:",os.getcwd())
    subprocess.Popen([f"rm -rf .git"],shell=True).wait()
    subprocess.Popen([f"git init"],shell=True).wait()
    subprocess.Popen([f"git add ."],shell=True).wait()
    subprocess.Popen([f"git commit -m 'production app'"],shell=True).wait()
    subprocess.Popen([f"git push --set-upstream git@"+pod_id+":root/juice-shop.git master"],shell=True).wait()

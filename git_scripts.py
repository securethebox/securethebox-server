"""
Git Scripts to make life easier
"""
import json
import subprocess
import sys
import os

class GitControl():
    def __init__(self):
        self.git_user = ""
        self.git_fork_name = ""
        self.git_prod_name = "securethebox"
        self.git_url = ""
        self.git_current_branch = ""
        self.git_upstream = ""
        self.arguments = []

    def setArguments(self, args):
        self.arguments = args

    def setGithubProjectUser(self):
        with open('./package.json',"r") as f:
            data = json.load(f)
            self.git_user = data["repository"]["url"].split('/')[3]
    
    def setGithubProjectName(self):
        with open('./package.json',"r") as f:
            data = json.load(f)
            self.git_fork_name = data["repository"]["url"].split('/')[4][:-4]
    
    def setCurrentGitBranch(self):
        branchName = subprocess.Popen("git branch | grep \\* | cut -d ' ' -f2", stdout=subprocess.PIPE, shell=True)
        parsedBranch = os.environ["CURRENTBRANCH"] = str(branchName.communicate()[0].decode('utf-8')).split('\n', 1)[0]
        self.git_current_branch = parsedBranch
    
    def interpretArgs(self):
        self.setGithubProjectName()
        self.setGithubProjectUser()
        self.setCurrentGitBranch()

        # Set environment type
        if self.arguments[0] == "dev":
            os.environ["APPENV"] = "DEV"
            subprocess.call("./venv/bin/python3.7 app.py",shell=True)
        elif self.arguments[0] == "prod":
            os.environ["APPENV"] = "PROD"
            subprocess.call("./venv/bin/python3.7 app.py",shell=True)

        # Pip Libraries
        elif self.arguments[0] == "pip-save":
            subprocess.call("./venv/bin/pip3 freeze > requirements.txt",shell=True)       
        
        # Pushing Master
        elif self.arguments[0] == "git-push-master":
            subprocess.Popen([f"git checkout master && git cz ; git push"],shell=True).wait()
        
        # Pushing Branch
        elif self.arguments[0] == "git-push-branch":
            if self.git_current_branch != "master":
                subprocess.Popen([f"git cz && git push --set-upstream origin "+self.git_current_branch+" && cross-var \"open https://github.com/"+self.git_user+"/"+self.git_fork_name+"/compare/master..."+self.git_user+":"+self.git_current_branch+"?expand=1\""],shell=True).wait()
            else:
                print("YOU ARE NOT CHECKOUT TO A BRANCH! git checkout -b \"TICKET-ID\"")
        
        # Sync Fork Master
        elif self.arguments[0] == "git-sync-local":
            subprocess.Popen([f"git checkout master ; git pull"],shell=True).wait()

        # Merge with Upstream
        elif self.arguments[0] == "git-merge-upstream":
            subprocess.Popen([f"git remote add upstream https://github.com/"+self.git_prod_name+"/"+self.git_fork_name+".git ; git fetch upstream ; git checkout master ; git merge upstream/master"],shell=True).wait()

if __name__ == "__main__":
    gc = GitControl()
    gc.setArguments(sys.argv[1:])
    gc.interpretArgs()
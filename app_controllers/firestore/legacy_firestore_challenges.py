import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from challenge_model import Challenge
from resource_model import Resource
from step_model import Step
import datetime

# Use a service account
cred = credentials.Certificate('../../secrets/firestore-stb-prod.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

"""
Challenge consists of Steps
Each Step contains:
- Overview
- Grading Critera
- Scenario
- Start Challenge
- Resources
- Submission
- Scoring

"""

def challenge_1(username):
    this_challenge = Challenge("Learning the Environment","Simulated business environment supporting security for an Application")
    this_challenge.category = "infrastructure"
    this_challenge.duration = 45
    this_challenge.difficulty = 3
    this_challenge.grading_criteria = ["vocal","ctf","definitions","video"]
    this_challenge.overview = "Gauging a cadidate's skill on infrastructure security"
    this_challenge.apps = ["juice-shop","splunk","nginx-modsecurity","gitlab","jenkins"]
    this_challenge.tags = ["interview","technical challenge","application security","infrastructure security"]

    # Create Step for 'Overview'
    step_overview_juice_shop = Step()
    step_overview_juice_shop.add_title("Overview")
    step_overview_juice_shop.add_block_of_text("This challenge assesses your skills in defending, responding, and preventing attacks against a web application.")
    


    # JUICE-SHOP
    resource_app_name = "juice-shop"
    resource_juice_shop = Resource()
    resource_juice_shop.edit_app_name("juice-shop")
    resource_juice_shop.edit_description("Main Application and most Valueable service. Keep this service up at all times apply your knowledge of security.")
    resource_juice_shop.edit_url("http://"+resource_app_name+"-"+username+".us-west1-a.securethebox.us/")
    resource_juice_shop.shell_url("http://"+resource_app_name+"-"+username+"-cloudcmd.us-west1-a.securethebox.us/")
    resource_juice_shop.add_credential("admin user", "admin@someemail.com", "admin123")
    resource_juice_shop.add_reference("Juice-Shop Source Code Repository","https://github.com/bkimminich/juice-shop")
    resource_juice_shop.add_reference("About Juice-Shop","https://www.owasp.org/index.php/OWASP_Juice_Shop_Project")
    resource_juice_shop.add_reference("Node-Vault node library","https://github.com/kr1sp1n/node-vault")
    resource_juice_shop.add_reference("Csurf CSRF token node library","https://github.com/expressjs/csurf")
    resource_juice_shop.add_reference("Content Security Policy (CSP) Cheatsheet","https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Content_Security_Policy_Cheat_Sheet.md")
    resource_juice_shop.add_tip("Frontend/Client = Angular.js")
    resource_juice_shop.add_tip("Backend/Server = Node.js+Express")
    resource_juice_shop.add_tip("Authentication = SQL+JWT")
    resource_juice_shop.add_tip("Change default passwords")
    resource_juice_shop.add_tip("Patch code in gitlab repository to fix vulnerabilities")
    resource_juice_shop.add_tip("Use Node-Vault library to request for secrets")
    resource_juice_shop.add_tip("Use CSurf middleware to add csrf token to requests")
    resource_juice_shop.add_tip("Change default passwords")

    # SPLUNK
    splunk_app = "splunk"
    this_challenge.add_resource(splunk_app,"Security Incident Event Management","http://splunk-"+username+".us-west1-a.securethebox.us/","http://splunk-"+username+"-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(splunk_app,"admin","Changeme")
    this_challenge.add_resource_reference(splunk_app,"Splunk Cheat Sheet","https://lzone.de/cheat-sheet/Splunk")
    this_challenge.add_resource_reference(splunk_app,"About Juice-Shop","https://www.owasp.org/index.php/OWASP_Juice_Shop_Project")
    this_challenge.add_resource_tip(splunk_app,"source=\"/var/log/challenge1/nginx-"+username+".log\"")
    this_challenge.add_resource_tip(splunk_app,"source=\"/var/log/challenge1/modsecurity-"+username+".log\"")
    this_challenge.add_resource_tip(splunk_app,"Set time frame of search to REAL-TIME 1 hour window.")
    this_challenge.add_resource_tip(splunk_app,"Adjust to Verbose Mode search.")
    this_challenge.add_resource_tip(splunk_app,"Consider the fields: status, http_method, uri_path, uri_query, http_user_agent, and http_referrer.")

    # NGINX-MODSECURITY
    nginx_modsecurity_app = "nginx-modsecurity"
    this_challenge.add_resource(nginx_modsecurity_app,"Load Balancer + Web Application Firewall","http://nginx-modsecurity-"+username+".us-west1-a.securethebox.us/","http://nginx-modsecurity-"+username+"-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(nginx_modsecurity_app,"none","none")
    this_challenge.add_resource_reference(nginx_modsecurity_app,"OWASP Core Rule Set","https://modsecurity.org/crs/")
    this_challenge.add_resource_tip(nginx_modsecurity_app,"source=\"/var/log/challenge1/nginx-"+username+".log\"")
    this_challenge.add_resource_tip(nginx_modsecurity_app,"source=\"/var/log/challenge1/modsecurity-"+username+".log\"")
    this_challenge.add_resource_tip(nginx_modsecurity_app,"To enable Modsecurity edit the /etc/nginx/nginx.conf file")
    this_challenge.add_resource_tip(nginx_modsecurity_app,"To modify Modsecurity edit /etc/nginx/modsec/modsecurity.conf file")
    this_challenge.add_resource_tip(nginx_modsecurity_app,"Reload nginx after changes with the command \"nginx -s reload\"")

    # GITLAB
    gitlab_app = "gitlab"
    this_challenge.add_resource(gitlab_app,"Source Code Respository","http://gitlab-"+username+".us-west1-a.securethebox.us/","http://gitlab-"+username+"-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(gitlab_app,"root","Changeme")
    this_challenge.add_resource_reference(gitlab_app,"Gitlab Git Cheatsheet","https://about.gitlab.com/images/press/git-cheat-sheet.pdf")
    this_challenge.add_resource_reference(gitlab_app,"Github Security Best Practices Cheat Sheet","https://snyk.io/blog/ten-git-hub-security-best-practices/")
    this_challenge.add_resource_tip(gitlab_app,"You can edit code directly from the Repository")
    this_challenge.add_resource_tip(gitlab_app,"Use Node-Vault to get Secrets")
    this_challenge.add_resource_tip(gitlab_app,"Create policies for read/write")

    # JENKINS
    jenkins_app = "jenkins"
    this_challenge.add_resource(jenkins_app,"Continuous Integration & Continuous Deployment Server","http://jenkins-"+username+".us-west1-a.securethebox.us/","http://jenkins-"+username+"-cloudcmd.us-west1-a.securethebox.us/")
    this_challenge.add_resource_credential(jenkins_app,"none","none")
    this_challenge.add_resource_reference(jenkins_app,"Jenkins Cheatsheet","https://www.edureka.co/blog/cheatsheets/jenkins-cheat-sheet/")
    this_challenge.add_resource_tip(jenkins_app,"When a changes happens in github project, jenkins run \"git pull\" command on juice-shop docker container to update changes to app")
    this_challenge.add_resource_tip(jenkins_app,"Edit the \"deploy-to-kubernetes\" job")
    this_challenge.add_resource_tip(jenkins_app,"Run \"Setup Security\" to add authentication")
    this_challenge.add_resource_tip(jenkins_app,"You do not need to \"build\" a docker image or \"deploy\", you just need to make changes in gitlab repository")

    # # HASHICORP VAULT
    # hashicorp_vault_index = 5

    # # HASHICORP CONSUL
    # hashicorp_consul_index = 6

    # QUESTIONS
    this_challenge.add_question("vocal", "What happens when you type the command \'wget www.google.com\'?")
    this_challenge.add_question("vocal", "How does SSL work between a client and server?")
    this_challenge.add_question("vocal", "What is the certificate chain of trust?")
    this_challenge.add_question("vocal", "What is confidentiality, integrity, and availablility mean in terms of security?")
    
    # this_challenge.save_challenge("charles",datetime.datetime.now(),"created challenge")
    # # TOPOLOGY
    # """
    # this should be pulled for a local file in the code base or ability to upload file
    # """
    this_challenge.print_challenge()

    # SAVE TO FIRESTORE
    db.collection(u'challenges').add(this_challenge.to_dict())
    # print(this_challenge.to_dict())


def test_challenge():
    this_challenge = Challenge("Learning the Environment","Simulated business environment supporting security for an Application")
    db.collection(u'challenges').add(this_challenge.to_dict())


if __name__ == "__main__":
    
    challenge_1("charles")
    # test_challenge()



"""
challenges -> id ->
    challenge_id
    challenge_title
    challenge_description
    challenge_overview
    challenge_published |
        - MM/DD/YYYY
    challenge_last_update |
        - MM/DD/YYYY
    challenge_difficulty |
        - Level 1 - 5
    challenge_tags: [] 
    challenge_category |
        - web applications
        - secrets management
        - git repository
        - ids/ips
        - tls/ssl, pki
        - operating system internals
        - code review
        - pentesting
        - infrastructure
        - cryptography
        - vpn
        - identity access management
        - incident response
        - forensics
        - business
        - leadership
    challenge_duration |
        - 10 minutes - 2 hours
    challenge_grading_criteria
        - must pass | 
            - coding
            - verbal
            - video
            - ctf
            - etc...
    challenge_enabled_apps
        - kali
        - gitlab
        - splunk
        - juice-shop
    challenge_scenario_topology
        - json format
    challenge_resources |
        url |
            - kali-"+username+".us-west1-a.securethebox.com
        shell |
            - kali-shell-"+username+".us-west1-a.securethebox.com
        credentials |
            - "+username+"
            - password
        references |
            - url1
        tips | 
            - tip1
    challenge_video_questions |
        - id
        - question_description
        - helper_attachments
        - helper_urls
        - helper_images
    challenge_vocal_questions
    challenge_coding_questions
    challenge_typed_questions
    challenge_ctf_questions
    challenge_video_submission
    challenge_vocal_submission
    challenge_coding_submission
    challenge_typed_submission
    challenge_ctf_submission


"""
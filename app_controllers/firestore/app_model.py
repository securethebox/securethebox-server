import datetime
import pprint

class App(object):
    def __init__(self):
        self.app_name = "Untitled"
        self.dockerhub_url = "https://hub.docker.com/r/username/appname"
        self.github_url = "https://github.com/ncmd/securethebox"
        self.kubernetes_deployment_files = []
        self.kubernetes_service_files = []
        self.kubernetes_ingress_files = []
        self.kubernetes_configmap_files = []
        self.kubernetes_bash_scripts = []
        self.kubernetes_python_scripts = []

    def set_app_name(self,app_name):
        self.app_name = app_name

    def set_dockerhub_url(self, dockerhub_url):
        self.dockerhub_url = dockerhub_url

    def set_github_url(self, github_url):
        self.github_url = github_url

    def add_kubernetes_deployment_file(self,file_path):
        self.kubernetes_deployment_files.append(file_path)

    def add_kubernetes_ingress_file(self,file_path):
        self.kubernetes_ingress_files.append(file_path)
    
    def add_kubernetes_service_file(self,file_path):
        self.kubernetes_service_files.append(file_path)

    def add_kubernetes_configmap_file(self,file_path):
        self.kubernetes_configmap_files.append(file_path)

    def print_app(self):
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.to_dict())

    def to_dict(self):
        this_dict = {
            u'app_name':self.app_name,
            u'dockerhub_url':self.dockerhub_url,
            u'github_url':self.github_url,
            u'kubernetes_deployment_file':self.kubernetes_deployment_files,
            u'kubernetes_ingress_file':self.kubernetes_ingress_files,
            u'kubernetes_service_file':self.kubernetes_service_files,
            u'kubernetes_configmap_files':self.kubernetes_configmap_files,
            u'kubernetes_bash_script':self.kubernetes_bash_scripts,
            u'kubernetes_python_script':self.kubernetes_python_scripts
        }

        return this_dict

    
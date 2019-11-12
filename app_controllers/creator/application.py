import yaml


class Application():
    def __init__(self):
        self.applicationList = []
        self.categories = {}

    def loadApplications(self, applicationList):
        self.applicationList = applicationList
        for app in self.applicationList:
            for key in app:
                if key == "category":
                    self.addCategory(app[key], app[key].replace("_"," ").capitalize() )

    def addApplication(self,applicationName):
        self.applicationList.append(applicationName)
        
    def getApplicationList(self):
        return self.applicationList
    
    def addCategory(self,category_v, category_l):
        self.categories[category_v] = category_l

    def getCategories(self):
        return self.categories

def generateDeploymentYaml(yamlData):
    # write to file.
    with open('./aws/s3/username/deployment.yaml','r+') as f:
        f.seek(0)
        try:
            yData = yaml.safe_load(yamlData)
            yaml.dump(yData, f, default_flow_style=False)
            # print("YDATA:",yData)
            # f.write(yData)
        except yaml.YAMLError as yError:
            print(yError)

def generateIngressYaml(yamlData):
    # write to file.
    with open('./aws/s3/username/ingress.yaml','w') as f:
        f.seek(0)
        try:
            yData = yaml.safe_load(yamlData)
            yaml.dump(yData, f, default_flow_style=False)
            # print("YDATA:",yData)
            # f.write(yData)
        except yaml.YAMLError as yError:
            print(yError)

def generateServiceYaml(yamlData):
    # write to file.
    with open('./aws/s3/username/service.yaml','w') as f:
        f.seek(0)
        try:
            yData = yaml.safe_load(yamlData)
            yaml.dump(yData, f, default_flow_style=False)
            # print("YDATA:",yData)
            # f.write(yData)
        except yaml.YAMLError as yError:
            print(yError)

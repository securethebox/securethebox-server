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

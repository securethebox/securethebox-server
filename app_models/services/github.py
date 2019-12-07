import sgqlc
"""
Setting github information

Not used for git cloning
"""

class Github:
    def __init__(self):
        self.respository_url = ""
        self.repository_name = "" 

    def setName(self, repository_name):
        self.repository_name = repository_name

    def setURL(self,respository_url):
        self.respository_url = respository_url

    def to_dict(self):
        this_dict = {
            u"github_name": self.repository_name,
            u"github_url": self.respository_url
        }
        return this_dict



    
    
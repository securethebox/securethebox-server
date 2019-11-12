


class Resource(object):
    def __init__(self):
        self.app_name = "Untitled"
        self.description = ""
        self.url = ""
        self.shell_url = ""
        self.credentials = []
        self.references = []
        self.tips = []
        
    def edit_app_name(self, new_name):
        self.app_name = new_name

    def edit_description(self, new_description):
        self.description = new_description
    
    def edit_url(self, new_url):
        self.url = new_url
    
    def edit_shell_url(self, new_shell_url):
        self.shell_url = new_shell_url

    def add_credential(self, title, username, password):
        self.credentials.append(
            {
                "credential_title" : title,
                "credential_username" : username,
                "credential_password" : password
            }
        )
    
    def add_reference(self, title, url):
        self.references.append(
            {
                "reference_title" : title,
                "reference_url" : url
            }
        )
    
    def add_tip(self,new_tip):
        self.tips.append(new_tip)

    def print_resource(self):
        print(self.references)
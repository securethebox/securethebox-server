class References:
    def __init__(self):
        self.references = []
    
    def addReference(self,reference_name, reference_url):
        self.references.append({
            "reference_name": reference_name,
            "reference_url": reference_url,
        })
    
    def to_dict(self):
        this_dict = {
            u"references": self.references
        }
        return this_dict
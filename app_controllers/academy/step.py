class Step(object):
    def __init__(self):
        self.id = ""
        self.title = ""
        self.content = ""
        self.stepDict = {}

    def setStep(self,cid,title,content):
        self.id = cid
        self.title = title
        self.content = content

    def to_dict(self):
        this_dict = {
            u"id":self.id,
            u"title":self.title,
            u"content":self.content
        }
        return this_dict
        
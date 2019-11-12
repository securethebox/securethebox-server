class Category(object):
    def __init__(self):
        self.id = 0,
        self.value = "",
        self.label = "",
        self.color = ""
    
    def setCategory(self,cid,value,label,color):
        self.id = cid
        self.value = value
        self.label = label
        self.color = color

    def to_dict(self):
        this_dict = {
            u"id":self.id,
            u"value":self.value,
            u"label":self.label,
            u"color":self.color,
        }
        return this_dict

    
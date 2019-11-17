class Application(object):
    def __init__(self):
        self.name = "",
        self.label = "",
        self.category = "",
        self.category_label = "",
        self.github = []
        self.references = []

    def to_dict(self):
        this_dict = {
            u"name":self.name,
            u"label":self.label,
            u"category":self.category,
            u"category_label":self.category_label,
            u"github":self.github,
            u"references":self.references
        }
        return this_dict

    
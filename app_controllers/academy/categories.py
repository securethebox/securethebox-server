class Categories(object):
    def __init__(self):
        self.categories = []
    
    def addCategory(self,category):
        self.categories.append(category)

    def getCategories(self):
        return self.categories

    def to_dict(self):
        this_dict = {
            u"categories":self.categories
        }
        return this_dict

    
class Steps(object):
    def __init__(self):
        self.steps = []

    def addStep(self,step):
        self.steps.append(step)
    
    def getSteps(self):
        return self.steps

    def to_dict(self):
        this_dict = {
            u"steps":self.steps
        }
        return this_dict

    
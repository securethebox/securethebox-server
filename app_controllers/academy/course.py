class Course(object):
    def __init__(self):
        self.id = 0,
        self.title = "",
        self.slug = "",
        self.description = "",
        self.category = ""
        self.length = ""
        self.totalSteps = ""
        self.activeStep = ""
        self.steps = []
    
    def setCourse(self,cid,title,slug,description,category,length,totalsteps,activestep,steps):
        self.id = cid
        self.title = title
        self.slug = slug
        self.description = description
        self.category = category
        self.length = length
        self.totalSteps = totalsteps
        self.activeStep = activestep
        self.steps = steps

    def to_dict(self):
        this_dict = {
            u"id":self.id,
            u"title":self.title,
            u"slug":self.slug,
            u"description":self.description,
            u"category":self.category,
            u"length":self.length,
            u"totalSteps":self.totalSteps,
            u"activeStep":self.activeStep,
            u"steps":self.steps,
        }
        return this_dict

    
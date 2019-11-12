class Courses(object):
    def __init__(self):
        self.courses = []

    def addCourse(self,course):
        self.courses.append(course)
    
    def getCourses(self):
        return self.courses

    def to_dict(self):
        this_dict = {
            u"courses":self.courses
        }
        return this_dict

    
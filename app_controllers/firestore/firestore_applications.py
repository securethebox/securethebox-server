import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from ..academy.categories import Categories
from ..academy.category import Category
from ..academy.course import Course
from ..academy.courses import Courses
from ..academy.step import Step
from ..academy.steps import Steps
import sys
import uuid

# Use a service account
cred = credentials.Certificate('./config/dev.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

class FirestoreAcademy():
    def __init__(self):
        self.courses = []
    
    def getCourses(self):
        docs = db.collection(u'academy').stream()
        courses = []
        for doc in docs:
            courses.append(doc.to_dict())
        self.courses = courses
        print(self.courses)
        return self.courses

    def addCourse(self, course_payload):
        _course = Course()
        _steps = Steps()
        
        for x in course_payload["steps"]:
            _steps.addStep(x)
        
        _course.setCourse(
            str(uuid.uuid4()),
            course_payload["title"],
            course_payload["title"].lower().replace(" ","-"),
            course_payload["description"],
            course_payload["category"],
            course_payload["length"],
            course_payload["totalSteps"],
            course_payload["activeStep"],
            _steps.getSteps())
        self.courses.append(_course.to_dict())
        db.collection(u'academy').add(_course.to_dict())
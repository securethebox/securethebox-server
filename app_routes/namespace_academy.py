from flask_restplus import Namespace, Resource, fields, reqparse
from .initialize.academy import main
from app_controllers.firestore.firestore_academy import FirestoreAcademy
import json

api = Namespace('academy', description='Academy related operations')

academy_parser = reqparse.RequestParser()
academy_parser.add_argument('courseId', help='{error_msg}')
academy_parser.add_argument('courseHandle', help='{error_msg}')

academy_course_update_parser = reqparse.RequestParser()
academy_course_update_parser.add_argument('id', help='{error_msg}')
academy_course_update_parser.add_argument('activeStep', type=int, help='{error_msg}')

academy_course_save_parser = reqparse.RequestParser()
academy_course_update_parser.add_argument('id', help='{error_msg}')
academy_course_save_parser.add_argument('data', help='{error_msg}')

course = api.model('Course', {
    'id': fields.String(required=True, description='The course identifier'),
})

categories, courses = main()
fa = FirestoreAcademy()
firestore_courses = fa.getCourses()

@api.route('/categories')
class AcademyCategories(Resource):
    @api.doc('get_categories')
    def get(self):
        # need backend to generate categories
        return categories, 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 


@api.route('/courses')
class AcademyCourses(Resource):
    @api.doc('get_courses')
    def get(self):
        return firestore_courses, 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 

@api.route('/course')
class AcademyCourse(Resource):
    @api.doc('get_course')
    def get(self):
        args = academy_parser.parse_args()
        try:
            for i in firestore_courses:
                if i["id"] == args['courseId']:
                    return i, 201, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 
        except:
            api.abort(404)

@api.route('/course/update')
@api.response(404, 'Course not found')
class AcademyCourseUpdate(Resource):
    @api.doc('update_course')
    def post(self):
        args = academy_course_update_parser.parse_args()
        try:
            for i,v in enumerate(firestore_courses):
                if v["id"] == args["id"]:
                    firestore_courses[i]["activeStep"] = args['activeStep']
                    return firestore_courses[i], 200 , {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
            return args
        except:
            return 404

@api.route('/course/save')
@api.response(404, 'Course not found')
class AcademyCourseSave(Resource):
    @api.doc('save_course')
    def post(self):
        args = academy_course_save_parser.parse_args()
        try:
            for i,v in enumerate(firestore_courses):
                if v["id"] == args["id"]:
                    firestore_courses[i] = args['data']
                    return firestore_courses[i],  201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
            return args
        except:
            return 404

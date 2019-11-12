from flask_restplus import Namespace, Resource, fields, reqparse
from .initialize.academy import main

api = Namespace('academy-app', description='Academy related operations')

academy_parser = reqparse.RequestParser()
academy_parser.add_argument('courseId', help='{error_msg}')
academy_parser.add_argument('courseHandle', help='{error_msg}')
academy_parser.add_argument('data', help='{error_msg}')

course = api.model('Course', {
    'id': fields.String(required=True, description='The course identifier'),
})

categories, courses = main()

@api.route('/categories')
class AcademyCategories(Resource):
    @api.doc('get_categories')
    def get(self):
        return categories, 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 

@api.route('/courses')
class AcademyCourses(Resource):
    @api.doc('get_courses')
    def get(self):
        return courses, 200, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 

@api.route('/course')
class AcademyCourse(Resource):
    @api.doc('get_course')
    def get(self):
        args = academy_parser.parse_args()
        try:
            for i in courses:
                if i["id"] == args['courseId']:
                    return i, 201, {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "GET"} 
        except:
            api.abort(404)

@api.route('/course/update')
@api.response(404, 'Course not found')
class AcademyCourseUpdate(Resource):
    @api.doc('update_course')
    @api.marshal_with(course)
    def post(self):
        args = academy_parser.parse_args()
        data = args["data"]
        try:
            for i in courses:
                if i["id"] == data["id"]:
                    return courses.update(data), 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
                else:
                    return i
        except:
            return 404

@api.route('/course/save')
@api.response(404, 'Course not found')
class AcademyCourseSave(Resource):
    @api.doc('save_course')
    @api.marshal_with(course)
    def post(self):
        args = academy_parser.parse_args()
        data = args['data']
        course = None
        try:
            for i in courses:
                if i["id"] == data["id"]:
                    course = data
                    return course, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
                return course, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
            if course is not None:
                course = data
                courses.append(course)
            return course, 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
        except:
            return 404

@api.route('/course/update')
@api.response(404, 'Course not found')
class AcademyCourse(Resource):
    @api.doc('update_course')
    @api.marshal_with(course)
    def post(self):
        args = academy_parser.parse_args()
        data = args["data"]
        try:
            for i in courses:
                if i["id"] == data["id"]:
                    return courses.update(data), 201 ,  {'Access-Control-Allow-Origin': '*', "Access-Control-Allow-Methods": "POST"} 
                else:
                    return i
        except:
            return 404

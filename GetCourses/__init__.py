import azure.functions as func
import json


def main(req: func.HttpRequest, courses: func.DocumentList) -> func.HttpResponse:
    course_list = []
    for course in courses.data:
        course_id = course.data['id']
        course_list.append(course_id)
    return func.HttpResponse(json.dumps(course_list))

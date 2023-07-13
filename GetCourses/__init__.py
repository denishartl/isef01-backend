import azure.functions as func
import json


def main(req: func.HttpRequest, courses: func.DocumentList) -> func.HttpResponse:

    # Returns a list of all tickets
    course_list = []
    for course in courses:
        course_data = {
            'id': course ['id'],
            'name': course ['name'],
            'shortname': course ['shortname'],
    }
        course_list.append(course_data)

    
        
    return func.HttpResponse(
        json.dumps(course_list),
        status_code=200
        )

import azure.functions as func
import json
import logging


def main(req: func.HttpRequest, courses: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Returns a list of all courses
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
    
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error course data could not be issued.",
            status_code=500
        )

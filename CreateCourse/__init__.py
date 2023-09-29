import logging
import uuid

import azure.functions as func

"""
This function creates a new document in the database based on the data passed in the JSON
body. 

Expected query parameters:
None

Expected content in the JSON body:
* course_name: Full name of the course
* course_shortname: Short name of the course
"""


def main(req: func.HttpRequest, course: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Check if every expected part of the request body exists
    try:
        req_body = req.get_json()
        if type(req_body) is str:
            return func.HttpResponse(
                'Body is not in JSON format. Please provide a valid JSON formated body.',
                status_code=400
            )
    except AttributeError:
        return func.HttpResponse(
            'No body provided. Please provide a JSON body.',
            status_code=400
        )
    else:
        course_shortname = req_body.get('course_shortname')
        course_name = req_body.get('course_name')

    # Return HTTP errors if one part of the body is missing
    try:
        if not course_shortname:
            return func.HttpResponse(
                'No course short name provided. Please provide a short name in the body when calling this function.',
                status_code=400
            )
        if not course_name:
            return func.HttpResponse(
                'No course name provided. Please provide a full course name in the body when calling this function.',
                status_code=400
            )

        # Save information to Azure CosmosDB
        course_dict = {
            'id': str(uuid.uuid1()),
            'shortname': course_shortname,
            'name': course_name
        }

        course.set(func.Document.from_dict(course_dict))
        return func.HttpResponse(
            status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )

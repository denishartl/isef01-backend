import azure.functions as func
import json
import logging


"""
This function returns a course based on the course shortname provided in the query parameter.

Expected query parameters:
* shortname: Short name of the course which should be returned
"""


def main(req: func.HttpRequest, course: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    course_shortname = req.params.get('shortname')
    if not course_shortname:
        return func.HttpResponse(
            "Please insert course shortname.",
            status_code=400
            )
    
    if not course:
        return func.HttpResponse(
             f"Could not find a course with the shortname {course_shortname}.",
              status_code=400
              )
    
    else:
        try:
            # Get course from CosmosDB via ticket_id
                course_doc = {
                    'id': course[0]['id'],
                    'shortname': course[0]['shortname'],
                    'name': course[0]['name']    
                }

                # Returns the course data as http response
                return func.HttpResponse(
                    json.dumps(course_doc),
                    status_code=200
                )
        
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                "Error finding course ID.",
                status_code=500
                )
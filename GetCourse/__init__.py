import azure.functions as func
import json
import logging


def main(req: func.HttpRequest, course: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    course_id = req.params.get('id')
    if not course_id:
        return func.HttpResponse(
            "Please insert course ID.",
            status_code=400
            )
    
    if not course:
        return func.HttpResponse(
             f"Could not find a course with the ID {course_id}.",
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
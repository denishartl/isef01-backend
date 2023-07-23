import azure.functions as func
import json
import logging


def main(req: func.HttpRequest, courses: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.max_retry_count)

    if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")

    try:
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
    
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error course data could not be issued.",
            status_code=500
        )

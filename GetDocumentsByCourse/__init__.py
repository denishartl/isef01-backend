import json
import logging
import azure.functions as func


"""
This function returns a list of documents based on the course ID provided in the query parameter.

Expected query parameters:
* course: ID of the course for which to return documents
"""


def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    course_id = req.params.get('course')
    if not course_id:
        return func.HttpResponse(
            "Please choose a course ID.",
            status_code=400
        )

    try:
        # Returns a list of all documents
        document_list = []
        for document in documents:
            document_data = {
                'id': document['id'],
                'title': document['title'],
                'doctype': document['doctype'],
                'course': document['course']
            }
            document_list.append(document_data)

        return func.HttpResponse(
            json.dumps(document_list),
            status_code=200
        )

    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error document data could not be issued.",
            status_code=500
        )

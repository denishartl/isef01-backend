import json
import logging
import azure.functions as func


def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    course_id = req.params.get('course')
    doctype = req.params.get('doctype')

    if not course_id:
        return func.HttpResponse(
            "Please choose a course ID.",
            status_code=400
        )

    try:
        # Filtering documents based on course ID and/or document type
        document_list = []
        for document in documents:
            if document['course'] == course_id and (not doctype or document['doctype'] == doctype):
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

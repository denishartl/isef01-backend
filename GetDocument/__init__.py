import json
import logging
import azure.functions as func


def main(req: func.HttpRequest, document: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    document_id = req.params.get('id')
    if not document_id:
        return func.HttpResponse(
            "Please choose a document ID.",
            status_code=400
        )

    if not document:
        return func.HttpResponse(
            f"Could not find document with ID {document_id}.",
            status_code=400
        )
    else:
        try:
            # Get document from CosmosDB via ticket_id and course_id
            document_doc = {
                'id': document[0]['id'],
                'title': document[0]['title'],
                'doctype': document[0]['doctype'],
            }

            return func.HttpResponse(
                json.dumps(document_doc),
                status_code=200
            )
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                "Error finding document ID.",
                status_code=500
            )

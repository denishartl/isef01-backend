import json
import logging
from xml.dom.minidom import Document

import azure.functions as func


def main(req: func.HttpRequest, attachment: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    document_id = req.params.get('id')
    if not document_id:
        return func.HttpResponse(
            "Please choose a document ID.",
            status_code=400
        )

    if not Document:
        return func.HttpResponse(
            f"Could not find attachment with ID {document_id}.",
            status_code=400
        )
    else:
        try:
            # Get course from CosmosDB via ticket_id and course_id

            document_doc = {
                'id': document[0]['id'],
                'title': document[0]['title'],
                'doctype': document[0]['doctype'],
            }

            return func.HttpResponse(
                json.dumps(document.doc),
                status_code=200
            )
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                "Error finding document ID.",
                status_code=500
            )

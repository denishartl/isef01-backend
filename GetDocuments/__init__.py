import json
import logging
import azure.functions as func


def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Returns a list of all documents
        document_list = []
        for document in documents:
            document_data = {
                'id': document['id'],
                'title': document['title'],
                'doctype': document['doctype'],
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

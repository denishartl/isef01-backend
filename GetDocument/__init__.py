import json
import logging
import azure.functions as func


def main(req: func.HttpRequest, document: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    document_id = req.params.get('id')
    if not document_id:
        return func.HttpResponse(
            "Please insert a document ID.",
            status_code=400
        )

    if not document:
        return func.HttpResponse(
             f"Could not find a document with the ID {document_id}.",
              status_code=404
              )
    
    else:
        try:
            # Get document from CosmosDB via document_id
                document_doc = {
                    'id': document[0]['id'],
                    'title': document[0]['title'],
                    'doctype': document[0]['doctype'],
                    'course' : document[0]['course']  
                }

                # Returns the document data as http response
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
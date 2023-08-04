import json
import logging
import azure.functions as func


def main(req: func.HttpRequest, attachment: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.max_retry_count)

   if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")

    try:
        # Returns a list of all documents
        document_list = []
        for document in documents:
            document_data = {
                'id': document[0]['id'],
                'title': document[0]['title'],
                'doctype': document[0]['doctype'],
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
import json
import logging

import azure.functions as func

"""
This function returns a specific attachment based on the ID provided in the query parameter:

Expected query parameters:
* id: ID of the attachment to return
"""

def main(req: func.HttpRequest, attachment: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.retry_count)


    if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")

    attachment_param_id = req.params.get('id')
    if not attachment_param_id:
        return func.HttpResponse(
            "Please provide a ticket ID to query for.",
            status_code=400
        )

    if not attachment:
        return func.HttpResponse(
            f"Could not find ticket with ID {attachment_param_id}.",
            status_code=400
        )
    else:
        try:
            attachment_json = {
                'id': attachment[0]['id'],
                'name': attachment[0]['name'],
                'ticket_id': attachment[0]['ticket_id'],
                'uuid': attachment[0]['uuid'],
                'blob_link': attachment[0]['blob_link']
            }

            return func.HttpResponse(
                json.dumps(attachment_json),
                status_code=200
            )
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                status_code=500
            )

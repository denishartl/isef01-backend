import json
import logging

import azure.functions as func

"""
This function returns a list of comments based on the ticket ID provided in the
query parameter.

Expected query parameters:
* ticket_id: ID of the ticket for which comments should be returnes
"""

def main(req: func.HttpRequest, comments: func.DocumentList, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.max_retry_count)

    if context.retry_context.retry_count == context.retry_context.max_retry_count:
        logging.warn(
            f"Max retries of {context.retry_context.max_retry_count} for "
            f"function {context.function_name} has been reached")
    
    ticket_id = req.params.get('ticket_id')
    if not ticket_id:
        return func.HttpResponse(
            "Please provide a ticket ID to query for.",
            status_code=400
        )
    
    if not comments:
        return func.HttpResponse(
            f"Could not find any comment for a ticket with ID {ticket_id}.",
            status_code=400
        )
    else:
        try:
            comment_list = []
            for comment in comments.data:
                comment_list.append(comment.data)
            return func.HttpResponse(
                json.dumps(comment_list),
                status_code=200
            )
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                status_code=500
            )

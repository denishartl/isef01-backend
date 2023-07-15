import datetime
import logging

import azure.functions as func

"""
This function creates a new comment in the database based on the data passed in the JSON
body. 

Expected query parameters:
None

Expected content in the JSON body:
* ticket_id: Ticket ID for which the comment should be created
* author_id: ID of the author creating the ticket
* text: comment text
"""

def main(req: func.HttpRequest, comment: func.Out[func.Document], context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('Current retry count: %s', context.retry_context.retry_count)

    if context.retry_context.retry_count == context.retry_context.max_retry_count:
            logging.warn(
                f"Max retries of {context.retry_context.max_retry_count} for "
                f"function {context.function_name} has been reached")
            
    # Check if every expected part of the request body exists
    try:
        req_body = req.get_json()
    except ValueError as ex:
        logging.error(ex)
        return func.HttpResponse(
            'No body provided. Please provide request body.',
            status_code=500
        )
    else:
        ticket_id = req_body.get('ticket_id')
        author_id = req_body.get('author_id')
        text = req_body.get('text')

    # Return HTTP errors if one part of the body is missing
    try:
        if not ticket_id:
            return func.HttpResponse(
                'No ticket ID provided. Please pass a ticket ID in the body when calling this function.',
                status_code=400
            )
        if not author_id:
            return func.HttpResponse(
                'No author ID provided. Please pass a author ID in the body when calling this function.',
                status_code=400
            )
        if not text:
            return func.HttpResponse(
                'No text provided. Please pass a text in the body when calling this function.',
                status_code=400
            )
    
        # Save information to Azure CosmosDB
        comment_dict = {
            'ticket': ticket_id,
            'author': author_id,
            'text': text,
            'createdAt': datetime.datetime.utcnow().isoformat()

        }

        comment.set(func.Document.from_dict(comment_dict))
        return func.HttpResponse(
                status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )

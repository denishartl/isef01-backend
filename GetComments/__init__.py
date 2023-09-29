import json
import logging

import azure.functions as func

"""
This function returns a list of comments based on the ticket ID provided in the
query parameter.

Expected query parameters:
* ticket_id: ID of the ticket for which comments should be returnes
"""

def get_createdAt(comment):
    return comment['createdAt']


def main(req: func.HttpRequest, comments: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
            comment_list.sort(key=get_createdAt, reverse=False)
            return func.HttpResponse(
                json.dumps(comment_list),
                status_code=200
            )
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                status_code=500
            )

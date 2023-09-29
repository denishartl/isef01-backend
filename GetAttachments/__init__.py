import json
import logging

import azure.functions as func

"""
This function returns a list of attachments based on the ticket ID provided in the query parameter:

Expected query parameters:
* ticket_id: ID of the ticket to return
"""


def main(req: func.HttpRequest, attachments: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    ticket_id = req.params.get('ticket_id')
    if not ticket_id:
        return func.HttpResponse(
            "Please provide a ticket ID to query for.",
            status_code=400
        )

    if not attachments:
        return func.HttpResponse(
            f"Could not find any attachment for a ticket with ID {ticket_id}.",
            status_code=400
        )
    else:
        try:
            attachment_list = []
            for attachment in attachments.data:
                attachment_list.append(attachment.data)
            return func.HttpResponse(
                json.dumps(attachment_list),
                status_code=200
            )
        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                status_code=500
            )

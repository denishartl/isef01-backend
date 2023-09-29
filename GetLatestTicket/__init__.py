import logging
import json
import azure.functions as func

"""
Selects the lastest Ticket based on creation date from CosmosDB
"""


def main(req: func.HttpRequest, ticket: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    if not ticket:
        return func.HttpResponse(
            "Could not fetch latest ticket.",
            status_code=500
        )
    else:
        try:
            # Get ticket from CosmosDB via ticket_id
            ticket_doc = {
                'id': ticket[0]['id'],
                'author_id': ticket[0]['author_id'],
                'course_id': ticket[0]['course_id'],
                'document_id': ticket[0]['document_id'],
                'ticket_type': ticket[0]['ticket_type'],
                'description': ticket[0]['description'],
                'status': ticket[0]['status'],
                'createdAt': ticket[0]['createdAt']

            }

            # Returns the ticket data as http response
            return func.HttpResponse(
                json.dumps(ticket_doc),
                status_code=200
            )

        except Exception as ex:
            logging.error(ex)
            return func.HttpResponse(
                "Error fetching latest ticket.",
                status_code=500
            )

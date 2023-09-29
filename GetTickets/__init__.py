import azure.functions as func
import json
import logging

"""

Returns a list of tickets based

"""


def main(req: func.HttpRequest, tickets: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Returns a list of all tickets
        ticket_list = []
        for ticket in tickets:
            ticket_data = {
                'id': ticket['id'],
                'author_id': ticket['author_id'],
                'course_id': ticket['course_id'],
                'document_id': ticket['document_id'],
                'ticket_type': ticket['ticket_type'],
                'description': ticket['description'],
                'status': ticket['status'],
                'createdAt': ticket['createdAt'],
                'assignee': ticket['assignee']
            }
            ticket_list.append(ticket_data)

        return func.HttpResponse(
            json.dumps(ticket_list),
            status_code=200
        )
    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            "Error ticket data could not be issued.",
            status_code=500
        )

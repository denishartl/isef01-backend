import azure.functions as func
import json

"""

Returns a list of tickets based on the ticket ID

Needed parameter: id (ticket)

"""

def main(req: func.HttpRequest, tickets: func.DocumentList) -> func.HttpResponse:
    ticket_id = req.params.get('id')


# Returns a list of all tickets
    ticket_list = []
    for ticket in tickets:
        ticket_data = {
            'id': ticket ['id'],
            'author_id': ticket ['author_id'],
            'course_id': ticket ['course_id'],
            'document_id': ticket ['document_id'],
            'ticket_type': ticket ['ticket_type'],
            'description': ticket ['description'],
            'status': ticket ['status'],
            'createdAt': ticket ['createdAt']
    }
        ticket_list.append(ticket_data)

    return func.HttpResponse(
        json.dumps(ticket_list),
        status_code=200
    )
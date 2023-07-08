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
        ticket_id = ticket['id']
        ticket_list.append(ticket_id)
        return func.HttpResponse(
            json.dumps(ticket_list),
            status_code=200
        )
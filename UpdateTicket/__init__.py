import datetime
import azure.functions as func
import json


def main(req: func.HttpRequest, ticket: func.DocumentList, outticket: func.Out[func.Document]) -> func.HttpResponse:
    ticket_id = req.params.get('id')

    # Get ticket from Cosmos DB
    if ticket:
        ticket_item = ticket[0]

        try:
            req_body = req.get_json()
        except ValueError:
            return func.HttpResponse(
                'Invalid JSON payload',
                status_code=400
            )
        # Update ticket data
        ticket_type = req_body.get('ticket_type')
        if ticket_type:
            ticket_item['ticket_type'] = ticket_type

        outticket.set(ticket_item)

        return func.HttpResponse(
            'Ticket updated successfully',
            status_code=200
        )
    else:
        return func.HttpResponse(
            'Ticket not found',
            status_code=404
        )
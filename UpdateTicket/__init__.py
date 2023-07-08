import azure.functions as func
import json


def main(req: func.HttpRequest, ticket: func.DocumentList) -> func.HttpResponse:
    ticket_id = req.params.get('id')

    # Get ticket from Cosmos DB
    if ticket:
        ticket_item = ticket[0]

        ticket_item['ticket_type'] = 'New Ticket Type'
        ticket_item['description'] = 'Updated description'

        return func.HttpResponse(
            'Ticket updated successfully',
            status_code=200
        )
    else:
        return func.HttpResponse(
            'Ticket not found',
            status_code=404
        )
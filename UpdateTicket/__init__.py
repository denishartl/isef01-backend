import datetime
import azure.functions as func


def main(req: func.HttpRequest, ticket: func.DocumentList, outticket: func.Out[func.Document]) -> func.HttpResponse:
    ticket_id = req.params.get('id')

    # Get ticket from Cosmos DB
    if ticket:
        ticket_item = ticket[0]

        ticket_item['ticket_type'] = 'New Ticket Type'
        ticket_item['description'] = 'Updated description'
        ticket_item['asignee'] = 'Pimmel'
        ticket_item['course_id'] = 'New ID'
        ticket_item['document_id'] = 'New document ID'
        ticket_item['changedAt'] = datetime.datetime.utcnow().isoformat()
        #status fehlt noch, der soll automatisch angepasst werden

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
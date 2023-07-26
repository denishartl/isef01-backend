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
        author_id = req_body.get('author_id')
        if author_id:
            ticket_item['author_id'] = author_id

        course_id = req_body.get('course_id')
        if course_id:
            ticket_item['course_id'] = course_id

        document_id = req_body.get('document_id')
        if document_id:
            ticket_item['document_id'] = document_id

        ticket_type = req_body.get('ticket_type')
        if ticket_type:
            ticket_item['ticket_type'] = ticket_type

        description = req_body.get('description')
        if description:
            ticket_item['description'] = description

        status = req_body.get('status')
        if status:
            ticket_item['status'] = status
            if status == "closed":
                ticket_item['resolvedAt'] = datetime.datetime.now().isoformat()

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
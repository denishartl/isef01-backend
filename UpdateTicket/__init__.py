import datetime
import azure.functions as func
import logging


def main(req: func.HttpRequest,
         ticket: func.DocumentList,
         outticket: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        ticket_id = req.params.get('ticket_id')
        if not ticket_id:
            return func.HttpResponse(
                "Please provide a Ticket ID to query for.",
                status_code=400
            )

        # Check if other requested parameters from the body exist
        try:
            req_body = req.get_json()
        except ValueError as ex:
            logging.error(ex)
            return func.HttpResponse(
                'No body provided. Please provide a request body.',
                status_code=500
            )

        # Get the ticket from Cosmos DB
        if ticket:
            ticket_item = ticket[0]

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

            assignee = req_body.get('assignee')
            if assignee:
                ticket_item['assignee'] = assignee

            status = req_body.get('status')
            if status:
                ticket_item['status'] = status
                if status == "closed":
                    ticket_item['resolvedAt'] = datetime.datetime.now(
                    ).isoformat()

            # Save the updated ticket
            outticket.set(ticket_item)

            return func.HttpResponse(
                ticket_id,
                status_code=200
            )
        else:
            return func.HttpResponse(
                'Ticket not found',
                status_code=404
            )

    except Exception as ex:
        logging.error(ex)
        return func.HttpResponse(
            status_code=500
        )
